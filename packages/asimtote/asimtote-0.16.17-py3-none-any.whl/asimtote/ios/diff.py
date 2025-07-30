# asimtote.ios.diff
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration differences module.

This module compares two configurations for Cisco IOS devices and
produces a delta configuration.
"""



# --- imports ---



import sys

from .converters import converters
from ..diff import DiffConfig, pathstr



# --- context parser ---



class CiscoIOSDiffConfig(DiffConfig):
    """This class is used to compare two IOS configuration files and
    generate a configuration file to transform one into the other.
    """


    def _init_blocks(self):
        "This method adds the converter block sequence for Cisco IOS."

        self._blocks = [
            # for interfaces being shut down, we do that before doing
            # any reconfiguration on them, in case the configuration is
            # disruptive
            "int-shutdown",

            # some changes must be done before things can be configured
            # that use them (e.g. HSRP version and high HSRP groups)
            "int-pre",

            # we don't need to do anything particular in advance
            None,

            # detect if there is a VRF change and, if so, make any
            # configuration updates required before we do the VRF change
            # itself
            "int-vrf-trigger", "int-vrf-pre",

            # now we actually do the VRF changes and trigger any
            # post-change actions (such as re-apply IP addresses)
            "int-vrf", "int-vrf-post",

            # some changes must be done after things use them have been
            # unconfigured (e.g. HSRP version and high HSRP groups)
            "int-post",

            # for route-map commands we need to delete all removed
            # entries before we insert any new ones - this is to avoid
            # clashes of match types, as well as ensure the action for
            # the entry ('permit' or 'deny') is not reset when removing
            # a later clauses as these change the entry
            "rtmap-del",
            "rtmap-add",
            "rtmap-add-cmty",

            # tracking objects are deleted in the 'None' block,
            # including if they are changing type; the new object is
            # then created, then the sub-configuration (which may need
            # to be triggered after a type change, to be reapplied)
            "track-create",
            "track-sub",

            # if changing a BGP neighbor peer-group, we need to delete
            # the neighbor first and recreate it, which means we need
            # to re apply the 'activate' with a trigger, so have to have
            # a separate block for that
            "bgp-nbr-activate",

            # if we remove a plain 'neighbor ... fall-over' command and
            # 'neighbor ... fall-over bfd' is configured, the BFD
            # command will also be removed and we need to reapply it
            "bgp-nbr-fallover-bfd",

            # if we're enabling interfaces, we do that after we've done
            # all the other configuration on them
            "int-noshutdown",
        ]


    def _add_converters(self):
        "This method adds the converters for Cisco IOS."

        for cvt_class in converters:
            try:
                self._add_converter(cvt_class())
            except:
                print("Exception in _add_converter(%s()) with:"
                          % cvt_class.__name__,
                      "",
                      file=sys.stderr)

                raise


    def _explain_comment(self, path):
        """This method overrides the empty inherited one to return a
        Cisco IOS comment giving the matched path.
        """

        return "! => " + pathstr(path)


    def _diffs_end(self):
        """This method overrides the empty inherited one to return a
        single line saying 'end'.
        """

        return ["end"]


    def init_rules_tree(self):
        """This method extends the inherited one to add some rules to
        the tree for the default CoPP (Control Plane Policing) IPv4
        extended and IPv6 ACLs.
        """

        super().init_rules_tree()

        self._rules_tree.update( {
            "ios-default": {
                "ip-access-list-extended": {
                    "acl-copp-match-igmp": {},
                    "acl-copp-match-pim-data": {},
                },
                "ipv6-access-list": {
                    "acl-copp-match-mld": {},
                    "acl-copp-match-ndv6": {},
                    "acl-copp-match-ndv6hl": {},
                    "acl-copp-match-pimv6-data": {},
                },
            },
        } )


    def init_rules_active(self):
        """This method extends the inherited one to add in some active
        rules to exclude the portions of the rules tree set up in
        init_rules_tree().
        """

        super().init_rules_active()

        self._rules_active.append( (False, ("ios-default", ) ) )
