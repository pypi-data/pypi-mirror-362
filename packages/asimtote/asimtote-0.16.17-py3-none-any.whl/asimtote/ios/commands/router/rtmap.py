# asimtote.ios.commands.router.rtmap
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault

from ....config import IndentedContextualCommand



# --- configuration command classes ---



# =============================================================================
# route-map ...
# =============================================================================



class Cmd_RtMap(IndentedContextualCommand):
    match = (r"route-map (?P<rtmap>\S+)( (?P<action>permit|deny))?"
             r"( (?P<seq>\d+))?")
    enter_context = "route-map"

    def parse(self, cfg, rtmap, action, seq):
        # if the sequence number is omitted, the route-map must either
        # be empty, in which case 10 is assumed, or have only one entry,
        # in which case that entry is modified

        if seq is None:
            if len(r) > 1:
                raise ValueError("route-map without sequence number and "
                                 "multiple existing entries")

            seq = 10 if len(r) == 0 else r[0]

        r = deepsetdefault(cfg, "route-map", rtmap, int(seq))

        # if no action is specified, 'permit' is assumed
        r["action"] = action or "permit"

        return r


class CmdContext_RtMap(IndentedContextualCommand):
    context = "route-map"


class Cmd_RtMap_MatchCmty(CmdContext_RtMap):
    match = r"match community (?P<cmtys>.+?)(?P<exact> exact-match)?"

    def parse(self, cfg, cmtys, exact):
        m = deepsetdefault(cfg, "match", "community")
        m.setdefault("communities", set()).update(cmtys.split(' '))
        if exact:
            m["exact-match"] = True


class Cmd_RtMap_MatchIPAddr(CmdContext_RtMap):
    match = r"match ip address(?P<pfx> prefix-list)? (?P<addrs>.+?)"

    def parse(self, cfg, pfx, addrs):
        # matching IP addresses can either be done by access-list (the
        # default) or prefix-list, but not both and one type cannot
        # directly be changed to another
        m = deepsetdefault(cfg, "match",
                           "ip-prefix-list" if pfx else "ip-address",
                           last=set())

        m.update(addrs.split(' '))


class Cmd_RtMap_MatchIPv6Addr(CmdContext_RtMap):
    match = r"match ipv6 address(?P<pfx> prefix-list)? (?P<addrs>.+?)"

    def parse(self, cfg, pfx, addrs):
        m = deepsetdefault(cfg, "match",
                           "ipv6-prefix-list" if pfx else "ipv6-address",
                           last=set())

        m.update(addrs.split(' '))


class Cmd_RtMap_MatchTag(CmdContext_RtMap):
    match = r"match tag (?P<tags>.+)"

    def parse(self, cfg, tags):
        m = deepsetdefault(cfg, "match", "tag", last=set())
        m.update(int(t) for t in tags.split(' '))


class Cmd_RtMap_SetCmty(CmdContext_RtMap):
    match = r"set community (?P<cmtys>.+?)(?P<add> additive)?"

    def parse(self, cfg, cmtys, add):
        s = deepsetdefault(cfg, "set", "community")
        s.setdefault("communities", set()).update(cmtys.split(' '))
        if add:
            s["additive"] = True


class Cmd_RtMap_SetIPNxtHop(CmdContext_RtMap):
    match = (r"set ip((?P<_global> global)| vrf (?P<vrf>\S+))? "
             r"next-hop (?P<addrs>[0-9. ]+)")

    def parse(self, cfg, _global, vrf, addrs):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        l = deepsetdefault(cfg, "set", "ip-next-hop", last=[])
        for addr in addrs.split(' '):
            nexthop = { "addr": addr }
            if _global or vrf:
                # the 'vrf' key is set if 'global' or a VRF is
                # specified for the next hop - if to global, the empty
                # string is used (we could use None but we're being
                # consistent with 'set global')
                nexthop["vrf"] = vrf or ""
            l.append(nexthop)


class Cmd_RtMap_SetIPNxtHopVrfy(CmdContext_RtMap):
    match = r"set ip next-hop verify-availability"

    def parse(self, cfg):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        deepsetdefault(cfg, "set")["ip-next-hop-verify-availability"] = True


class Cmd_RtMap_SetIPNxtHopVrfyTrk(CmdContext_RtMap):
    match = (r"set ip next-hop verify-availability (?P<addr>[0-9.]+) "
             r"(?P<seq>\d+) track (?P<obj>\d+)")

    def parse(self, cfg, addr, seq, obj):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        v = deepsetdefault(cfg, "set", "ip-next-hop-verify-availability-track")
        v[int(seq)] = {
            "addr": addr,
            "track-obj": int(obj)
        }


class Cmd_RtMap_SetIPv6NxtHop(CmdContext_RtMap):
    match = r"set ipv6 next-hop (?P<addrs>[0-9a-f: ]+)"

    def parse(self, cfg, addrs):
        # the next-hop addresses are a list, built up in the order
        # they're specified, optionally with a named or global VRF
        l = deepsetdefault(cfg, "set", "ipv6-next-hop", last=[])
        for addr in addrs.split(' '):
            # we don't really need to use a dictionary here, but it
            # keeps it consistent with the IPv4 version, in case extra
            # options are added in future
            l.append({ "addr": addr })


class Cmd_RtMap_SetLocalPref(CmdContext_RtMap):
    match = r"set local-preference (?P<pref>\d+)"

    def parse(self, cfg, pref):
        cfg.setdefault("set", {})["local-preference"] = int(pref)


class Cmd_RtMap_SetVRF(CmdContext_RtMap):
    # this handles both 'set global' and 'set vrf ...'
    match = r"set (global|vrf (?P<vrf>\S+))"

    def parse(self, cfg, vrf):
        # the global routing table is indicated by an empty string VRF
        # setting
        deepsetdefault(cfg, "set", "vrf", last=vrf or "")
