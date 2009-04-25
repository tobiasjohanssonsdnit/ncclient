# Copyright 2009 Shikhar Bhushan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from xml.etree import cElementTree as ET

from common import BASE_NS
from common import qualify as _

try:
    register_namespace = ET.register_namespace
except AttributeError:
    def register_namespace(prefix, uri):
        from xml.etree import ElementTree
        # cElementTree uses ElementTree's _namespace_map
        ElementTree._namespace_map[uri] = prefix

register_namespace('netconf', BASE_NS)

class TreeBuilder:
    '''Build an ElementTree.Element instance from an XML tree specification
    based on nested dictionaries.
    '''
    
    def __init__(self, spec):
        self._root = TreeBuilder.build(spec)
        
    def to_string(self, encoding='utf-8'):
        # etree does not include the <?xml..?> processing instruction
        # if encoding is utf-8. this is a problem with cisco routers.
        prepend = '<?xml version="1.0" encoding="UTF-8"?>' if encoding=='utf-8' else ''
        return prepend + ET.tostring(self._root, encoding)
    
    @property
    def tree(self):
        return self._root
    
    @staticmethod
    def build(spec):
        'Returns constructed ElementTree.Element'
        if spec.has_key('tag'):
            ele = ET.Element(spec.get('tag'), spec.get('attributes', {}))
            ele.text = spec.get('text', '')
            children = spec.get('children', [])
            if isinstance(children, dict):
                children = [children]
            for child in children:
                ele.append(TreeBuilder.build(child))
            return ele
        elif spec.has_key('comment'):
            return ET.Comment(spec.get('comment'))
        else:
            raise ValueError('Invalid tree spec')


class HelloBuilder:
        
    @staticmethod
    def build(capabilities, encoding='utf-8'):
        children = [{'tag': 'capability', 'text': uri } for uri in capabilities]
        spec = {
            'tag': _('hello', BASE_NS),
            'children': [{
                        'tag': u'capabilities',
                        'children': children
                        }]
            }
        return TreeBuilder(spec).to_string(encoding)

class RPCBuilder:
    
    @staticmethod
    def build(msgid, op, encoding='utf-8'):
        if isinstance(op, basestring):
            return RPCBuilder.build_from_string(msgid, op, encoding)
        else:
            return RPCBuilder.build_from_spec(msgid, op, encoding)
    
    @staticmethod
    def build_from_spec(msgid, opspec, encoding='utf-8'):
        spec = {
            'tag': _('rpc', BASE_NS),
            'attributes': {'message-id': msgid},
            'children': opspec
            }
        return TreeBuilder(spec).to_string(encoding)
    
    @staticmethod
    def build_from_string(msgid, opstr, encoding='utf-8'):
        decl = '<?xml version="1.0" encoding="%s"?>' % encoding
        doc = (u'''<rpc message-id="%s" xmlns="%s">%s</rpc>''' %
               (msgid, BASE_NS, opstr)).encode(encoding)
        return (decl + doc)