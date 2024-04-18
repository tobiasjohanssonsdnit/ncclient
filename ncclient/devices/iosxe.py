"""
Handler for Cisco IOS-XE device specific information.

Note that for proper import, the classname has to be:

    "<Devicename>DeviceHandler"

...where <Devicename> is something like "Default", "Nexus", etc.

All device-specific handlers derive from the DefaultDeviceHandler, which implements the
generic information needed for interaction with a Netconf server.

"""

from .default import DefaultDeviceHandler

from ncclient.operations.third_party.iosxe.rpc import (
    SaveConfig,
    SyncFromRunningToConfD,
    CurrentTime,
    IsSyncing,
    Revert,
    Rollback,
    Checkpoint,
    NetconfSessionId,
)
from ncclient.xml_ import BASE_NS_1_0

import logging

logger = logging.getLogger("ncclient.devices.iosxe")


def iosxe_unknown_host_cb(host, fingerprint):
    # This will ignore the unknown host check when connecting to CSR devices
    return True


class IosxeDeviceHandler(DefaultDeviceHandler):
    """
    Cisco IOS-XE handler for device specific information.
    """

    def __init__(self, device_params):
        super(IosxeDeviceHandler, self).__init__(device_params)

    def add_additional_operations(self):
        """Return all the additional operations"""

        return {
            "save_config": SaveConfig,
            "sync_from": SyncFromRunningToConfD,
            "current_time": CurrentTime,
            "is_syncing": IsSyncing,
            "rollback": Rollback,
            "checkpoint": Checkpoint,
            "revert": Revert,
            "netconf_session_id": NetconfSessionId,
        }

    def add_additional_ssh_connect_params(self, kwargs):
        kwargs["unknown_host_cb"] = iosxe_unknown_host_cb

    def transform_edit_config(self, node):
        # find the first node that has the tag "config" with no namespace
        nodes = node.findall("./config")
        if len(nodes) == 1:
            logger.debug("IOS XE handler: patching namespace of config element")
            nodes[0].tag = "{%s}%s" % (BASE_NS_1_0, "config")
        return node
