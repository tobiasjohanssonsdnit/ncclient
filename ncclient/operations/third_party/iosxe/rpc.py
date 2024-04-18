from lxml import etree

from ncclient.xml_ import *
from ncclient.operations.rpc import RPC


class SaveConfig(RPC):
    """Copy the running-config to startup-config on the Network Element"""

    def request(self):
        node = etree.Element(qualify("save-config", "http://cisco.com/yang/cisco-ia"))
        return self._request(node)


class IsSyncing(RPC):
    """Get the syncing status of the network element"""

    def request(self):
        node = etree.Element(qualify("is-syncing", "http://cisco.com/yang/cisco-ia"))
        return self._request(node)


class CurrentTime(RPC):
    """Get the current time on the network element"""

    def request(self):
        node = etree.Element(qualify("current-time", "http://cisco.com/yang/cisco-ia"))
        return self._request(node)


class NetconfSessionId(RPC):
    """get the network element's assigned netconf session id"""

    def request(self):
        node = etree.Element(
            qualify("netconf-session-id", "http://cisco.com/yang/cisco-ia")
        )
        return self._request(node)


class Checkpoint(RPC):
    """Create a configuration rollback checkpoint"""

    def request(self):
        node = etree.Element(qualify("checkpoint", "http://cisco.com/yang/cisco-ia"))
        return self._request(node)


class SyncFromRunningToConfD(RPC):
    """Synchronize the network element's running-configuration to ConfD"""

    def request(self, input: dict = {}):
        node = etree.Element(qualify("sync-from", "http://cisco.com/yang/cisco-ia"))
        return self._request(node)


class Revert(RPC):
    """Cancel the timed rollback and trigger rollback, or modify the timed rollback"""

    def request(self, input: dict = {}):
        node = etree.Element(qualify("revert", "http://cisco.com/yang/cisco-ia"))
        return self._request(node)


class Rollback(RPC):
    """Cancel the timed rollback and trigger rollback, or modify the timed rollback"""

    def request(self, input: dict = {}):
        node = etree.Element(qualify("rollback", "http://cisco.com/yang/cisco-ia"))
        return self._request(node)
