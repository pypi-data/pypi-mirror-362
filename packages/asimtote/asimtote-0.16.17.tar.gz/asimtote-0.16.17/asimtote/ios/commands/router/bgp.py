# asimtote.ios.commands.router.bgp
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault
import netaddr

from ...utils import VRF_GLOBAL
from ....config import IndentedContextualCommand



# --- functions ---



def neighbor_canonicalize(nbr):
    """Canonicalise a BGP neighbor identifier - these can be descriptive
    names (for a peer-group) or an IP address.  In the case of IPv6, we
    need to ensure the case is consistent, so we upper case it.

    If the name is not an IPv6 address, we return it as-is.
    """

    if netaddr.valid_ipv6(nbr):
        return str(netaddr.IPAddress(nbr, 6)).upper()

    return nbr



# --- configuration command classes ---



# =============================================================================
# router bgp ...
# =============================================================================



class Cmd_RtrBGP(IndentedContextualCommand):
    # ASNs can be in 'n' as well as 'n.n' format so we can't just use an
    # integer
    match = r"router bgp (?P<asn>\d+(\.\d+)?)"
    enter_context = "router-bgp"

    def parse(self, cfg, asn):
        return deepsetdefault(cfg, "router", "bgp", asn)


class CmdContext_RtrBGP(IndentedContextualCommand):
    context = "router-bgp"


class Cmd_RtrBGP_BGPRtrID(CmdContext_RtrBGP):
    match = r"bgp router-id (?P<id>\S+)"

    def parse(self, cfg, id):
        cfg["router-id"] = id


class Cmd_RtrBGP_NbrFallOver_BFD(CmdContext_RtrBGP):
    match = (r"neighbor (?P<nbr>\S+) fall-over bfd"
             r"( (?P<bfd>single-hop|multi-hop))?")

    def parse(self, cfg, nbr, bfd):
        deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                           "fall-over")["bfd"] = bfd


class Cmd_RtrBGP_NbrFallOver_Route(CmdContext_RtrBGP):
    match = (r"neighbor (?P<nbr>\S+) fall-over"
             r"( route-map (?P<rtmap>\S+))?")

    def parse(self, cfg, nbr, rtmap):
        r = deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                               "fall-over", "route")
        if rtmap:
            r["route-map"] = rtmap


class Cmd_RtrBGP_NbrPwd(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) password( (?P<enc>\d)) (?P<pwd>\S+)"

    def parse(self, cfg, nbr, enc, pwd):
        deepsetdefault(
            cfg["neighbor"][neighbor_canonicalize(nbr)])["password"] = {
                "encryption": int(enc), "password": pwd
            }


class Cmd_RtrBGP_NbrPrGrp(CmdContext_RtrBGP):
    # this class matches the creation of a peer-group
    match = r"neighbor (?P<nbr>\S+) peer-group"

    def parse(self, cfg, nbr):
        # this creates a neighbor as a peer-group
        #
        # unlike most commands that configure neighbors and require them
        # to exist (by using 'cfg["neighbor"][...(nbr)]), this will
        # create a new neighbor using a path with deepsetdefault()
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["type"] = "peer-group"


class Cmd_RtrBGP_NbrPrGrpMbr(CmdContext_RtrBGP):
    # this class matches the addition of a member to a peer-group
    match = r"neighbor (?P<nbr>\S+) peer-group (?P<grp>\S+)"

    def parse(self, cfg, nbr, grp):
        # this creates a neighbor as a member of a peer-group
        #
        # unlike most commands that configure neighbors and require them
        # to exist (by using 'cfg["neighbor"][...(nbr)]), this will
        # create a new neighbor using a path with deepsetdefault()
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["peer-group"] = grp


class Cmd_RtrBGP_NbrRemAS(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) remote-as (?P<rem_asn>\d+(\.\d+)?)"

    def parse(self, cfg, nbr, rem_asn):
        # this creates a new neighbor host
        #
        # unlike most commands that configure neighbors and require them
        # to exist (by using 'cfg["neighbor"][...(nbr)]), this will
        # create a new neighbor using a path with deepsetdefault()
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["remote-as"] = rem_asn


class Cmd_RtrBGP_NbrUpdSrc(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) update-source (?P<int_name>\S+)"

    def parse(self, cfg, nbr, int_name):
        deepsetdefault(
            cfg["neighbor"][neighbor_canonicalize(nbr)])["update-source"] = (
                int_name)



# =============================================================================
# router bgp ... address-family ... [vrf ...]
# =============================================================================



class Cmd_RtrBGP_AF(CmdContext_RtrBGP):
    # this regexp will match 'vpnv[46] vrf ...' which is illegal, but we're
    # not trying to validate commands
    match = (r"address-family (?P<af>ipv[46]( (?P<cast>unicast|multicast))?|"
             r"vpnv4|vpnv6)( vrf (?P<vrf>\S+))?")

    enter_context = "router-bgp-af"

    def parse(self, cfg, af, cast, vrf):
        # unicast/multicast is optional - if omitted, we assume unicast
        if not cast:
            af += " unicast"

        # we put addres families in the global routing table in a VRF
        # called VRF_GLOBAL
        return deepsetdefault(
                   cfg, "vrf", vrf or VRF_GLOBAL, "address-family", af)


class CmdContext_RtrBGP_AF(IndentedContextualCommand):
    context = "router-bgp-af"


class Cmd_RtrBGP_AF_NbtAct(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) activate"

    def parse(self, cfg, nbr):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["activate"] = True


class Cmd_RtrBGP_AF_NbrAddPath(CmdContext_RtrBGP_AF):
    # 'receive' must come after 'send'; 'disable' exclusive
    match = (r"neighbor (?P<nbr>\S+) additional-paths"
             r"(( (?P<snd>send))?( (?P<rcv>receive))?|( (?P<dis>disable)))")

    def parse(self, cfg, nbr, snd, rcv, dis):
        # additional paths is a set of all matching types (or 'disable')
        deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))[
            "additional-paths"] = { a for a in (snd, rcv, dis) if a }


class Cmd_RtrBGP_AF_NbrAdvAddPath(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) advertise additional-paths"
             r"(?=.*\s(?P<all>all))?"
             r"(?=.*\s(best( (?P<best_n>\d+))))?"
             r"(?=.*\s(?P<grp_best>group-best))?"
             r".+")

    def parse(self, cfg, nbr, all, best_n, grp_best):
        a = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr),
                           "advertise-additional-paths")

        if all:
            a["all"] = True
        if best_n:
            a["best"] = int(best_n)
        if grp_best:
            a["group-best"] = True


class Cmd_RtrBGP_AF_NbrAlwAS(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) allowas-in( (?P<max>\d+))?"

    def parse(self, cfg, nbr, max):
        # we can't just use None for an empty 'allowas-in' maximum as
        # this cannot be changed to, as a different type
        n = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))
        a = {}
        if max is not None:
            a["max"] = int(max)
        n["allowas-in"] = a


class Cmd_RtrBGP_AF_NbrFallOver_BFD(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) fall-over bfd"
             r"( (?P<bfd>single-hop|multi-hop))?")

    def parse(self, cfg, nbr, bfd):
        deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                           "fall-over")["bfd"] = bfd


class Cmd_RtrBGP_AF_NbrFallOver_Route(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) fall-over"
             r"( route-map (?P<rtmap>\S+))?")

    def parse(self, cfg, nbr, rtmap):
        r = deepsetdefault(cfg["neighbor"][neighbor_canonicalize(nbr)],
                               "fall-over", "route")
        if rtmap:
            r["route-map"] = rtmap


class Cmd_RtrBGP_AF_NbrFltLst(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) filter-list (?P<list_>\d+)"
             r" (?P<dir_>in|out)")

    def parse(self, cfg, nbr, list_, dir_):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr), "filter-list")[
                dir_] = int(list_)


class Cmd_RtrBGP_AF_NbrMaxPfx(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) maximum-prefix (?P<max>\d+)"
             r"( (?P<thresh>\d+))?")

    def parse(self, cfg, nbr, max, thresh):
        m = deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr), "maximum-prefix")
        m["max"] = int(max)
        if thresh:
            m["threshold"] = int(thresh)


class Cmd_RtrBGP_AF_NbrNHSelf(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) next-hop-self(?P<all> all)?"

    def parse(self, cfg, nbr, all):
        n = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))
        h = {}
        if all:
            h["all"] = True
        n["next-hop-self"] = h


class Cmd_RtrBGP_AF_NbrPrGrp(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) peer-group"

    def parse(self, cfg, nbr):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["type"] = "peer-group"


class Cmd_RtrBGP_AF_NbrPrGrpMbr(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) peer-group (?P<grp>\S+)"

    def parse(self, cfg, nbr, grp):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["peer-group"] = grp


class Cmd_RtrBGP_AF_NbrPfxLst(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) prefix-list (?P<list_>\S+)"
             r" (?P<dir_>in|out)")

    def parse(self, cfg, nbr, list_, dir_):
        deepsetdefault(cfg, "neighbor", nbr, "prefix-list")[dir_] = list_


class Cmd_RtrBGP_AF_NbrPwd(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) password( (?P<enc>\d)) (?P<pwd>\S+)"

    def parse(self, cfg, nbr, enc, pwd):
        deepsetdefault(
            cfg["neighbor"][neighbor_canonicalize(nbr)])["password"] = {
                "encryption": int(enc), "password": pwd
            }


class Cmd_RtrBGP_AF_NbrRemAs(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) remote-as (?P<rem_asn>\d+(\.\d+)?)"

    def parse(self, cfg, nbr, rem_asn):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))["remote-as"] = rem_asn


class Cmd_RtrBGP_AF_NbrRemPrivAS(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) remove-private-as(?P<all> all)?"

    def parse(self, cfg, nbr, all):
        n = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr))
        r = {}
        if all:
            r["all"] = True
        n["remove-private-as"] = r


class Cmd_RtrBGP_AF_NbrRtMap(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) route-map (?P<rtmap>\S+) (?P<dir_>in|out)"

    def parse(self, cfg, nbr, rtmap, dir_):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr), "route-map")[dir_] = (
                rtmap)


class Cmd_RtrBGP_AF_NbrSndCmty(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) send-community"
             r"( (?P<cmty>standard|extended|both))?")

    def parse(self, cfg, nbr, cmty):
        # this command adjusts the current state of the setting rather
        # than replacing it (e.g. entering "extended" when only
        # "standard" is set will change to "both")
        #
        # we don't worry about that but track each setting independently
        c = deepsetdefault(cfg, "neighbor", neighbor_canonicalize(nbr),
                           "send-community", last=set())
        if cmty in (None, "standard", "both"):
            c.add("standard")
        if cmty in ("extended", "both"):
            c.add("extended")


class Cmd_RtrBGP_AF_NbrSoftRecfg(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) soft-reconfiguration inbound"

    def parse(self, cfg, nbr):
        deepsetdefault(
            cfg, "neighbor", neighbor_canonicalize(nbr))[
                "soft-reconfiguration"] = "inbound"


class Cmd_RtrBGP_AF_MaxPaths(CmdContext_RtrBGP_AF):
    match = r"maximum-paths (?P<paths>\d+)"

    def parse(self, cfg, paths):
        cfg["maximum-paths"] = int(paths)


class Cmd_RtrBGP_AF_MaxPathsIBGP(CmdContext_RtrBGP_AF):
    match = r"maximum-paths ibgp (?P<paths>\d+)"

    def parse(self, cfg, paths):
        cfg["maximum-paths-ibgp"] = int(paths)


class Cmd_RtrBGP_AF_Redist_Plain(CmdContext_RtrBGP_AF):
    match = (r"redistribute (?P<proto>static|connected)"
             r"( route-map (?P<rtmap>\S+))?( metric (?P<met>\d+))?")

    def parse(self, cfg, proto, rtmap, met):
        r = deepsetdefault(cfg, "redistribute", proto)
        if rtmap:
            r["route-map"] = rtmap
        if met:
            r["metric"] = int(met)


class Cmd_RtrBGP_AF_Redist_OSPF(CmdContext_RtrBGP_AF):
    match = (r"redistribute (?P<proto>ospf|ospfv3) (?P<proc>\d+)"
             r"( route-map (?P<rtmap>\S+))?( metric (?P<met>\d+))?")

    def parse(self, cfg, proto, proc, rtmap, met):
        r = deepsetdefault(cfg, "redistribute", proto, int(proc))
        if rtmap:
            r["route-map"] = rtmap
        if met:
            r["metric"] = int(met)
