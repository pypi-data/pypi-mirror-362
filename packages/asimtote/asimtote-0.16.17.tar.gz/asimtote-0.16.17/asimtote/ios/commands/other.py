# asimtote.ios.commands.other
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault, deepget
import netaddr

from ..utils import expand_set, interface_canonicalize
from ...config import IndentedContextualCommand



# --- configuration command classes ---



# =============================================================================
# system
# =============================================================================



class Cmd_Comment(IndentedContextualCommand):
    # we don't really need to match comments as they do nothing but it
    # avoids chugging through the entire list of commands and doing
    # nothing
    match = r"!.*"


class Cmd_Hostname(IndentedContextualCommand):
    match = r"hostname (?P<hostname>\S+)"

    def parse(self, cfg, hostname):
        cfg["hostname"] = hostname


class Cmd_SNMPServer_Contact(IndentedContextualCommand):
    match = r"snmp-server contact (?P<contact>.+)"

    def parse(self, cfg, contact):
        cfg.setdefault("snmp-server", {})["contact"] = contact


class Cmd_SNMPServer_Location(IndentedContextualCommand):
    match = r"snmp-server location (?P<location>.+)"

    def parse(self, cfg, location):
        cfg.setdefault("snmp-server", {})["location"] = location



# =============================================================================
# [no] spanning-tree ...
# =============================================================================



class Cmd_NoSTP(IndentedContextualCommand):
    match = r"no spanning-tree vlan (?P<tags>[-0-9,]+)"

    def parse(self, cfg, tags):
        cfg.setdefault(
            "no-spanning-tree-vlan", set()).update(expand_set(tags))


class Cmd_STPPri(IndentedContextualCommand):
    match = r"spanning-tree vlan (?P<tags>[-0-9,]+) priority (?P<pri>\d+)"

    def parse(self, cfg, tags, pri):
        cfg_stp_pri = cfg.setdefault("spanning-tree-vlan-priority", {})
        for tag in expand_set(tags):
            cfg_stp_pri[int(tag)] = int(pri)



# =============================================================================
# track ...
# =============================================================================



class Cmd_TrackModify(IndentedContextualCommand):
    match = r"track (?P<obj>\d+)"
    enter_context = "track"

    def parse(self, cfg, obj):
        # if there is no criterion, we're modifying an existing object,
        # which must have already been defined, so we deliberately don't
        # create it with deepsetdefault() but just deepget() it with
        # default_error set, to force an error here, if it doesn't exist
        return deepget(cfg, "track", int(obj), default_error=True)


class Cmd_TrackInt(IndentedContextualCommand):
    match = (r"track (?P<obj>\d+) interface (?P<interface>\S+)"
             r" (?P<capability>(ip|ipv6) routing|line-protocol)")
    enter_context = "track"

    def parse(self, cfg, obj, interface, capability):
        t = deepsetdefault(cfg, "track", int(obj))
        t.clear()
        t.update({
            "type": "interface",
            "interface": {
                "interface": interface_canonicalize(interface),
                "capability": capability,
            }
        })
        return t


class Cmd_TrackList(IndentedContextualCommand):
    match = r"track (?P<track_num>\d+) list boolean (?P<op>and|or)"
    enter_context = "track"

    def parse(self, cfg, track_num, op):
        t = deepsetdefault(cfg, "track", int(track_num))
        t.update({
            "type": "list",
            "list": {
                "type": "boolean",
                "op": op,
            }
        })
        return t


class Cmd_TrackRoute(IndentedContextualCommand):
    match = (r"track (?P<track_num>\d+)"
             r" (?P<proto>ip|ipv6) route"
             r" (?P<net>[0-9a-fA-F.:]+/\d+|[0-9.]+ [0-9.]+)"
             r" (?P<measure>metric threshold|reachability)")
    enter_context = "track"

    def parse(self, cfg, track_num, proto, net, measure):
        # the 'net' can be in 'network netmask' or CIDR format, but the
        # netaddr.IPNetwork() object requires a slash between the
        # network and netmask, so we just change the space to a slash
        net = str(netaddr.IPNetwork(net.replace(' ', '/')))

        t = deepsetdefault(cfg, "track", int(track_num))
        t.clear()
        t.update({
            "type": "route",
            "route": {
                "proto": proto,
                "net": net,
                "measure": measure,
            }
        })
        return t


# although there are several different subcontexts, depends on the type of
# track, when extending a track with list 'track <num>' above, we don't know
# what it is, so just put all the commands in one context


class CmdContext_Track(IndentedContextualCommand):
    context = "track"


class Cmd_Track_Delay(CmdContext_Track):
    # 'up' and 'down' can appear in either order and are optional, as
    # long as one of them is present
    match = (r"delay(?=.* up (?P<up>\d+))?(?=.* down (?P<down>\d+))?"
             r"( (up|down) \d+)( (up|down) \d+)?")

    def parse(self, cfg, up, down):
        d = deepsetdefault(cfg, "delay")
        if up:
            d["up"] = int(up)
        if down:
            d["down"] = int(down)


class Cmd_Track_IPVRF(CmdContext_Track):
    match = r"ip vrf (?P<vrf_name>\S+)"

    def parse(self, cfg, vrf_name):
        cfg["ip-vrf"] = vrf_name


class Cmd_Track_IPv6VRF(CmdContext_Track):
    match = r"ipv6 vrf (?P<vrf_name>\S+)"

    def parse(self, cfg, vrf_name):
        cfg["ipv6-vrf"] = vrf_name


class Cmd_Track_Obj(CmdContext_Track):
    match = r"object (?P<obj>.+)"

    def parse(self, cfg, obj):
        deepsetdefault(cfg, "object", last=set()).add(int(obj))



# =============================================================================
# vlan ...
# =============================================================================



class Cmd_VLAN(IndentedContextualCommand):
    match = r"vlan (?P<tag>\d+)"
    enter_context = "vlan"

    def parse(self, cfg, tag):
        # create the VLAN configuration entry, setting an 'exists' key
        # as we might stop other information in here that isn't in the
        # VLAN definition itself in IOS (e.g. STP priority) in future
        v = deepsetdefault(cfg, "vlan", int(tag))
        v["exists"] = True

        return v


class CmdContext_VLAN(IndentedContextualCommand):
    context = "vlan"


class Cmd_VLAN_Name(CmdContext_VLAN):
    # VLAN names can have spaces in but we chop off any trailing spaces
    # in the parse() method
    match = r"name (?P<name>.+)"

    def parse(self, cfg, name):
        cfg["name"] = name.strip()



# =============================================================================
# vrf ...
# =============================================================================



class Cmd_VRF(IndentedContextualCommand):
    match = r"vrf definition (?P<name>\S+)"
    enter_context = "vrf"

    def parse(self, cfg, name):
        return deepsetdefault(cfg, "vrf", name)


class CmdContext_VRF(IndentedContextualCommand):
    context = "vrf"


class Cmd_VRF_RD(CmdContext_VRF):
    match = r"rd (?P<rd>(\d+|\d+\.\d+\.\d+\.\d+):\d+)"

    def parse(self, cfg, rd):
        cfg["rd"] = rd


class Cmd_VRF_RT(CmdContext_VRF):
    match = (r"route-target (?P<dir_>import|export|both)"
             r" (?P<rt>((\d+|\d+\.\d+\.\d+\.\d+):\d+))")

    def parse(self, cfg, dir_, rt):
        if dir_ in { "import", "both" }:
            deepsetdefault(cfg, "route-target", "import", last=set()).add(rt)
        if dir_ in { "export", "both" }:
            deepsetdefault(cfg, "route-target", "export", last=set()).add(rt)


class Cmd_VRF_AF(CmdContext_VRF):
    # "unicast" on the end is effectively ignored
    match = r"address-family (?P<af>ipv4|ipv6)( unicast)?"
    enter_context = "vrf-af"

    def parse(self, cfg, af):
        return deepsetdefault(cfg, "address-family", af)


class CmdContext_VRF_AF(IndentedContextualCommand):
    context = "vrf-af"


class Cmd_VRF_AF_RT(CmdContext_VRF_AF):
    match = (r"route-target (?P<dir_>import|export|both)"
             r" (?P<rt>(\d+|\d+\.\d+\.\d+\.\d+):\d+)")

    def parse(self, cfg, dir_, rt):
        if dir_ in { "import", "both" }:
            deepsetdefault(cfg, "route-target", "import", last=set()).add(rt)
        if dir_ in { "export", "both" }:
            deepsetdefault(cfg, "route-target", "export", last=set()).add(rt)
