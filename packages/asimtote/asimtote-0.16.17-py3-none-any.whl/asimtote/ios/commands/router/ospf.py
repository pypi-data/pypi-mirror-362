# asimtote.ios.commands.router.ospf
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault

from ...utils import interface_canonicalize
from ....config import IndentedContextualCommand



# --- configuration command classes ---



# =============================================================================
# router ospf ...
# =============================================================================



# this function is used for both ospf and ospfv3 so is shared

def _ospf_passive_interface(cfg, int_name, passive):
    """This function maintains a "passive-interface" dictionary under
    the supplied configuration (cfg) for OSPF or an OSPFv3 address
    family.

    The named interface (int_name) is set to either passive or active.

    If the interface name is the literal "default" then the default
    interface status is changed.
    """

    # create the "passive-interface" dictionary, if it doesn't exist
    p = cfg.setdefault("passive-interface", {})


    if int_name == "default":
        # we're changing the default

        if passive:
            # we're making passive interfaces the default so we don't
            # need to keep a list of passive interfaces, if there is one
            p["default"] = True
            if "interface" in p:
                p.pop("interface")
        else:
            # the opposite of the above
            if "default" in p:
                p.pop("default")
            if "no-interface" in p:
                p.pop("no-interface")

    else:
        # we're changing an individual interface

        # the name of the set of interfaces we're adjusting depends on
        # whether this interface is being configured as passive or
        # active
        int_set_key = "interface" if passive else "no-interface"

        ic = interface_canonicalize(int_name)
        if passive != p.get("default", False):
            # we're setting an interface state to the opposite of the
            # default - add it to the exception list
            deepsetdefault(p, int_set_key, last=set()).add(ic)

        else:
            # we're setting an interface to the same state as the
            # default - remove it from the exception set, if it exists
            if int_set_key in p:
                p[int_set_key].discard(ic)

                # if the set is now empty, we remove it completely
                if not p.get(int_set_key):
                    p.pop(int_set_key)


    # if the passive interface configuration is now empty (which means
    # we have active interfaces by default with no exceptions), remove
    # the whole passive interface configuration dictionary
    if not p:
        cfg.pop("passive-interface")



class Cmd_RtrOSPF(IndentedContextualCommand):
    match = r"router ospf (?P<proc>\d+)"
    enter_context = "router-ospf"

    def parse(self, cfg, proc):
        return deepsetdefault(cfg, "router", "ospf", int(proc))


class CmdContext_RtrOSPF(IndentedContextualCommand):
    context = "router-ospf"


class Cmd_RtrOSPF_ID(CmdContext_RtrOSPF):
    match = r"router-id (?P<id_>[.0-9]+)"

    def parse(self, cfg, id_):
        cfg["id"] = id_


class Cmd_RtrOSPF_AreaNSSA(CmdContext_RtrOSPF):
    match = (r"area (?P<area>\S[.0-9]+)"
             r" nssa(?P<no_redist> no-redistribution)?"
             r"(?P<no_summ> no-summary)?")

    def parse(self, cfg, area, no_redist, no_summ):
        n = deepsetdefault(cfg, "area", area, "nssa", last=set())
        if no_redist:
            n.add("no-redistribution")
        if no_summ:
            n.add("no-summary")


class Cmd_RtrOSPF_PasvInt(CmdContext_RtrOSPF):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        _ospf_passive_interface(cfg, int_name, not no)



# =============================================================================
# router ospfv3 ...
# =============================================================================



class Cmd_RtrOSPFv3(IndentedContextualCommand):
    match = r"router ospfv3 (?P<proc>\d+)"
    enter_context = "router-ospfv3"

    def parse(self, cfg, proc):
        return deepsetdefault(cfg, "router", "ospfv3", int(proc))


class CmdContext_RtrOSPFv3(IndentedContextualCommand):
    context = "router-ospfv3"


class Cmd_RtrOSPFv3_Id(CmdContext_RtrOSPFv3):
    match = r"router-id (?P<id_>[.0-9]+)"

    def parse(self, cfg, id_):
        cfg["id"] = id_


class Cmd_RtrOSPFv3_AreaNSSA(CmdContext_RtrOSPFv3):
    match = (r"area (?P<area>\S[.0-9]+)"
             r" nssa(?P<no_redist> no-redistribution)?"
             r"(?P<no_summ> no-summary)?")

    def parse(self, cfg, area, no_redist, no_summ):
        n = deepsetdefault(cfg, "area", area, "nssa", last=set())
        if no_redist:
            n.add("no-redistribution")
        if no_summ:
            n.add("no-summary")


class Cmd_RtrOSPFv3_AF(CmdContext_RtrOSPFv3):
    # "unicast" on the end is effectively ignored
    match = r"address-family (?P<af>ipv4|ipv6)( unicast)?"
    enter_context = "router-ospfv3-af"

    def parse(self, cfg, af):
        return deepsetdefault(cfg, "address-family", af)


class CmdContext_RtrOSPFv3_AF(CmdContext_RtrOSPFv3):
    context = "router-ospfv3-af"


class Cmd_RtrOSPFv3_AF_PasvInt(CmdContext_RtrOSPFv3_AF):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        _ospf_passive_interface(cfg, int_name, not no)


class Cmd_RtrOSPFv3_PasvInt(CmdContext_RtrOSPFv3):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        # the handling of this command outside of an address-family
        # block is a bit odd - it isn't stored at the router process
        # level but in the address family block and only affects the
        # currently defined address families, so if an address family
        # is added later, this will not propagate down
        for af in cfg.get("address-family", []):
            _ospf_passive_interface(
                cfg["address-family"][af], int_name, not no)
