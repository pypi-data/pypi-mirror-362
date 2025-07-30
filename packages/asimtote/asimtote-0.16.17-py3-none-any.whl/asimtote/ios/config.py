# asimtote.ios.config
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration module.

This module parses Cisco IOS configuration files into a dictionary.
"""



# --- imports ---



from ..config import IndentedContextualConfig

from .commands import commands
from .utils import seq_to_list, ip_acl_std_canonicalize



# --- constants ---



# this dictionary specifies the settings in a portchannel interface
# which will propagate out to the member interfaces
#
# these settings are copied from the portchannel interface to the
# member interfaces, after a configuration is read

INTERFACE_PORTCHANNEL_MEMBER_CFG = [
    "storm-control",
    "switchport",
    "switchport-mode",
    "switchport-nonegotiate",
    "switchport-trunk-native",
    "switchport-trunk-allow",
]



# --- classes ----



class CiscoIOSConfig(IndentedContextualConfig):
    "This concrete class parses Cisco IOS configuration files."


    def _add_commands(self):
        """This method is called by the constructor to add commands for
        the IOS platform.

        The commands are stored in a global (to the module) level list
        of classes.
        """

        for cmd_class in commands:
            self._add_command(cmd_class)


    def _post_parse(self):
        """Extend the inherited method to flush any pending IPv4
        standard ACL rules into the configuration.
        """

        super()._post_parse()


        # IPv4 standard ACLs are parsed into the "ip-access-list-
        # standard-seq" dictionary keyed on the sequence number; when
        # we've finished reading in the configuration file, we turn this
        # into a list "ip-access-list-standard", sorted by sequence
        # number and only containing the rules themselves

        if "ip-access-list-standard-seq" in self:
            acls_seq = self["ip-access-list-standard-seq"]
            acls_list = self.setdefault("ip-access-list-standard", {})

            for name in acls_seq:
                # if we've already read an ACL with this name, we
                # cannot convert it a second time (arguably we should,
                # but it would involve retaining the original sequenced
                # ACL and we tidy that away to avoid cluttering the
                # exposed configuration with an internal intermediate
                # structure)
                if name in acls_list:
                    raise NotImplementedError(
                              "IP access-list standard name: %s "
                              "already read - cannot update" % name)

                acls_list[name] = ip_acl_std_canonicalize(
                                     seq_to_list(acls_seq[name]))

            # when we're done, we remove the dictionary keyed on
            # sequence number
            self.pop("ip-access-list-standard-seq")


        # IPv4 extended ACLs are handled the same as standard ACLs,
        # above, except we don't need to canonicalise the rules

        if "ip-access-list-extended-seq" in self:
            acls_seq = self["ip-access-list-extended-seq"]
            acls_list = self.setdefault("ip-access-list-extended", {})

            for name in acls_seq:
                if name in acls_list:
                    raise NotImplementedError(
                              "IP access-list extended name: %s "
                              "already read - cannot update" % name)

                acls_list[name] = seq_to_list(acls_seq[name])

            self.pop("ip-access-list-extended-seq")


        # IPv6 ACLs are handled in the same way as IPv4 extended ACLs

        if "ipv6-access-list-seq" in self:
            acls_seq = self["ipv6-access-list-seq"]
            acls_list = self.setdefault("ipv6-access-list", {})

            for name in acls_seq:
                if name in acls_list:
                    raise NotImplementedError(
                              "IPv6 access-list name: %s already ready "
                              "- cannot update" % name)

                acls_list[name] = seq_to_list(acls_seq[name])

            self.pop("ipv6-access-list-seq")


        # IPv4 and IPv6 prefix lists are handled in the same way as IPv4
        # extended ACLs

        if "ip-prefix-list-seq" in self:
            acls_seq = self["ip-prefix-list-seq"]
            acls_list = self.setdefault("ip-prefix-list", {})

            for name in acls_seq:
                if name in acls_list:
                    raise NotImplementedError(
                              "IP prefix-list name: %s already read "
                              "- cannot update" % name)

                acls_list[name] = seq_to_list(acls_seq[name])

            self.pop("ip-prefix-list-seq")

        if "ipv6-prefix-list-seq" in self:
            acls_seq = self["ipv6-prefix-list-seq"]
            acls_list = self.setdefault("ipv6-prefix-list", {})

            for name in acls_seq:
                if name in acls_list:
                    raise NotImplementedError(
                              "IPv6 prefix-list name: %s already read "
                              "- cannot update" % name)

                acls_list[name] = seq_to_list(acls_seq[name])

            self.pop("ipv6-prefix-list-seq")


        # go through the interfaces and copy settings from the
        # portchannel interface, if that interface is a member of one

        for int_name in self.get("interface", {}):
            # get the dictionary for this interface

            int_ = self["interface"][int_name]


            # if this interface is a portchannel member ...

            if "channel-group" in int_:
                id_ = int_["channel-group"][0]


                # get the corresponding portchannel interface this is a
                # member of

                po_int = self["interface"].get("Po%d" % id_, {})


                # copy the settings which propagate to the members into
                # this interface

                for setting in INTERFACE_PORTCHANNEL_MEMBER_CFG:
                    if setting in po_int:
                        int_[setting] = po_int[setting]
