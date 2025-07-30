# asimtote.ios.converters.router.bgp
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from ....diff import Convert
from ...utils import VRF_GLOBAL



# --- converter classes ---



# =============================================================================
# router bgp ...
# =============================================================================



class Cvt_RtrBGP(Convert):
    cmd = "router", "bgp", None

    def remove(self, old, c, asn):
        return "no router bgp " + asn

    def add(self, new, c, asn):
        return "router bgp " + asn


class Context_RtrBGP(Convert):
    context = Cvt_RtrBGP.cmd

    def enter(self, asn):
        return ["router bgp " + asn]


class Cvt_RtrBGP_BGPRtrID(Context_RtrBGP):
    cmd = "router-id",

    def remove(self, old, c):
        return self.enter(*c) + [" no bgp router-id"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" bgp router-id " + new]


class Cvt_RtrBGP_Nbr(Context_RtrBGP):
    cmd = "neighbor", None

    def remove(self, old, c, nbr):
        # when removing a neighbor that is a peer-group, we need to
        # state that
        return self.enter(*c) + [
                   "  no neighbor "
                       + nbr
                       + (" peer-group" if old.get("type") == "peer-group"
                              else "")]

    def add(self, new, c, nbr):
        # we only explicitly need to add a neighbor if it's a peer-group
        # (normally, a neighbor is created implicitly by configuring
        # settings for it, starting by putting it in a peer-group or
        # its remote-as)
        if new.get("type") == "peer-group":
            return self.enter(*c) + ["  neighbor %s peer-group" % nbr]


class Context_RtrBGP_Nbr(Context_RtrBGP):
    context = Context_RtrBGP.context + Cvt_RtrBGP_Nbr.cmd

    # we're going to use these classes directly under the 'router,bgp,
    # ASN,neighbor,NBR' context and the 'router,bgp,ASN,vrf,VRF,
    # address-family,AF,neighbor,NBR' context but we also need access to
    # the NBR parameter for the commands (since they start 'neighbor
    # NBR ...')
    #
    # setting context_offset to -1 causes the neighbor to be supplied as
    # a local argument to the converter and gives a variable length
    # context, depending on whether the configuration is at the global
    # or address-family level
    context_offset = -1


class Cvt_RtrBGP_Nbr_FallOver(Context_RtrBGP_Nbr):
    cmd = "fall-over",

    def remove(self, old, c, nbr):
        return self.enter(*c) + [" no neighbor %s fall-over" % nbr]


class Context_RtrBGP_Nbr_FallOver(Context_RtrBGP_Nbr):
    context = Context_RtrBGP_Nbr.context + Cvt_RtrBGP_Nbr_FallOver.cmd


class Cvt_RtrBGP_Nbr_FallOver_BFD(Context_RtrBGP_Nbr_FallOver):
    cmd = "bfd",
    block = "bgp-nbr-fallover-bfd"

    def remove(self, old, c, nbr):
        return self.enter(*c) + [" no neighbor %s fall-over bfd" % nbr]

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [
                   " neighbor %s fall-over bfd%s"
                       % (nbr, (' ' + new) if new else "")]


class Cvt_RtrBGP_Nbr_FallOver_Route(Context_RtrBGP_Nbr_FallOver):
    cmd = "route",
    trigger_blocks = { "bgp-nbr-fallover-bfd" }

    def _cmd(self, nbr, rtmap):
        return ("neighbor %s fall-over%s"
                    % (nbr, (" route-map " + rtmap) if rtmap else ""))

    def remove(self, old, c, nbr):
        return (
            self.enter(*c)
            + [ " no " + self._cmd(nbr, old.get("route-map")) ])

    def truncate(self, old, rem, new, c, nbr):
        l = self.enter(*c)

        # if there was a route-map but we're changing to the plain form
        # of the command, we can't just remove it but have to remove the
        # entire command and then add the plain form
        if ("route-map" in ({} if old is None else old)
            and ("route-map" not in new)):

            l.append(" no " + self._cmd(nbr, old["route-map"]))

        l.append(' ' + self._cmd(nbr, new.get("route-map")))

        return l

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [ ' ' + self._cmd(nbr, new.get("route-map")) ]

    def trigger_set_filter_delete(self, t, old, rem, new, c, nbr):
        # if we're removing a plain fall-over command (with no
        # route-map), we need to reapply the 'fall-over bfd' command, if
        # that was present
        return "route-map" not in old

    def trigger_set_filter_update(self, *_):
        # we never need to trigger on updates
        return False


class Cvt_RtrBGP_Nbr_Pwd(Context_RtrBGP_Nbr):
    cmd = "password",

    def remove(self, old, c, nbr):
        return self.enter(*c) + [" no neighbor %s password" % nbr]

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [
                   " neighbor %s password %d %s"
                       % (nbr, new["encryption"], new["password"])]


class Cvt_RtrBGP_Nbr_PrGrpMbr(Context_RtrBGP_Nbr):
    # this converter is used to add or remove a neighbor to/from a
    # peer-group
    cmd = "peer-group",
    trigger_blocks = { "bgp-nbr-activate" }

    def remove(self, old, c, nbr):
        return self.enter(*c) + ["  no neighbor %s peer-group %s" % (nbr, old)]

    def add(self, new, c, nbr):
        return self.enter(*c) + ["  neighbor %s peer-group %s" % (nbr, new)]

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [
                   "  no neighbor %s peer-group %s" % (nbr, old),
                   "  neighbor %s peer-group %s" % (nbr, new)]


class Cvt_RtrBGP_Nbr_RemAS(Context_RtrBGP_Nbr):
    cmd = "remote-as",
    sort_key = "0_remote-as",

    # removing a remote AS actually removes the neighbor, so we deal
    # with that in the context, above - we just handle add/update here

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [" neighbor %s remote-as %s" % (nbr, new)]


class Cvt_RtrBGP_Nbr_UpdSrc(Context_RtrBGP_Nbr):
    cmd = "update-source",

    def remove(self, old, c, nbr):
        return self.enter(*c) + [" no neighbor %s update-source" % nbr]

    def update(self, old, upd,new, c, nbr):
        return self.enter(*c) + [" neighbor %s update-source %s" % (nbr, new)]


# router bgp ... address-family ... [vrf ...]


# working out the address-family line is complicated and we do it in
# several places, so separate it into a function

def _RtrBGP_AF_cmd(vrf, af):
    # address families in the global routing table as in a VRF called
    # VRF_GLOBAL as a special case so everything lines up at the same
    # level in the inventory
    return (" address-family "
            + af
            + ((" vrf " + vrf) if vrf != VRF_GLOBAL else ""))


class Cvt_RtrBGP_AF(Context_RtrBGP):
    cmd = "vrf", None, "address-family", None

    def remove(self, old, c, vrf, af):
        return self.enter(*c) + [" no" + _RtrBGP_AF_cmd(vrf, af)]

    def add(self, new, c, vrf, af):
        return self.enter(*c) + [_RtrBGP_AF_cmd(vrf, af)]


class Context_RtrBGP_AF(Context_RtrBGP):
    context = Context_RtrBGP.context + Cvt_RtrBGP_AF.cmd

    def enter(self, *c):
        c_super, (vrf, af) = c[:-2], c[-2:]
        return super().enter(*c_super) + [_RtrBGP_AF_cmd(vrf, af)]


class Cvt_RtrBGP_AF_MaxPaths(Context_RtrBGP_AF):
    cmd = "maximum-paths",

    def remove(self, old, c):
        return self.enter(*c) + ["  no maximum-paths %d" % old]

    def update(self, old, upd, new, c):
        return self.enter(*c) + ["  maximum-paths %d" % new]


class Cvt_RtrBGP_AF_MaxPathsIBGP(Context_RtrBGP_AF):
    cmd = "maximum-paths-ibgp",

    def remove(self, old, c):
        return self.enter(*c) + ["  no maximum-paths ibgp %d" % old]

    def update(self, old, upd, new, c):
        return self.enter(*c) + ["  maximum-paths ibgp %d" % new]


# 'redistribute' is a single line command but operates more as a
# context and so is handled as one, although, unlike the 'neighbor ...'
# commands does not need to be handled different from global vs VRF
# address families, so we don't need two versions
#
# entering 'redistribute ...' will enable redistribution and 'no
# redistribute ...' will turn it off again
#
# configuring 'route-map' or 'metric' will turn these settings on, and
# enable redistribution at the same time (if it is not already)
#
# 'no redistribute ... route-map/metric' will turn them off, but leave
# redistribution itself on


# classes to cover the redistribution contexts


class Cvt_RtrBGP_AF_Redist_Simple(Context_RtrBGP_AF):
    cmd = "redistribute", { "static", "connected" }

    def remove(self, old, c, proto):
        return self.enter(*c) + ["  no redistribute " + proto]

    def add(self, new, c, proto):
        return self.enter(*c) + ["  redistribute " + proto]


class Cvt_RtrBGP_AF_Redist_OSPF(Context_RtrBGP_AF):
    cmd = "redistribute", { "ospf", "ospfv3" }, None

    def remove(self, old, c, proto, proc):
        return self.enter(*c) + ["  no redistribute %s %d" % (proto, proc)]

    def add(self, new, c, proto, proc):
        return self.enter(*c) + ["  redistribute %s %d" % (proto, proc)]


# context versions of above
#
# the parameter classes will be subclasses of these and use a variable
# length context because the 'simple' protocols have no additional
# arguments but the OSPF one has a process number


class Context_RtrBGP_AF_Redist_Simple(Context_RtrBGP_AF):
    context = Context_RtrBGP_AF.context + Cvt_RtrBGP_AF_Redist_Simple.cmd

    # also get the protocol from the context
    context_offset = -1

    def _redist(self, proto):
        return "redistribute " + proto


class Context_RtrBGP_AF_Redist_OSPF(Context_RtrBGP_AF):
    context = Context_RtrBGP_AF.context + Cvt_RtrBGP_AF_Redist_OSPF.cmd

    # also get the protocol and process number from the context
    context_offset = -2

    def _redist(self, proto, proc):
        return "redistribute %s %d" % (proto, proc)


# redistribution parameter classes


class Cvt_RtrBGP_AF_Redist_Simple_Metric(Context_RtrBGP_AF_Redist_Simple):
    cmd = "metric",

    def remove(self, old, c, *redist):
        return self.enter(*c) + ["  no %s metric" % self._redist(*redist)]

    def update(self, old, upd, new, c, *redist):
        return self.enter(*c) + [
                   "  %s metric %d" % (self._redist(*redist), new)]


class Cvt_RtrBGP_AF_Redist_Simple_RtMap(Context_RtrBGP_AF_Redist_Simple):
    cmd = "route-map",

    def remove(self, old, c, redist):
        return self.enter(*c) + [
                   "  no %s route-map %s" % (self._redist(redist), old)]

    def update(self, old, upd, new, c, redist):
        return self.enter(*c) + [
                   "  %s route-map %s" % (self._redist(redist), new)]


# OSPF version of the above parameter classes - these inherit from the
# OSPF context class, instead of the simple context class


class Cvt_RtrBGP_AF_Redist_OSPF_Metric(
    Context_RtrBGP_AF_Redist_OSPF, Cvt_RtrBGP_AF_Redist_Simple_Metric):

    pass


class Cvt_RtrBGP_AF_Redist_OSPF_RtMap(
    Context_RtrBGP_AF_Redist_OSPF, Cvt_RtrBGP_AF_Redist_Simple_RtMap):

    pass


# adding and removing entire neighbors as a context is only done in the
# non-global VRF (in the global VRF, neighbors are configured at the
# parent, 'router bgp' level and then only address-family specific
# parameters at that level; for VRFs, the whole neighbor, including the
# remote-as, is configured at the address-family level)

class Cvt_RtrBGP_AF_vrf_Nbr(Context_RtrBGP_AF, Cvt_RtrBGP_Nbr):
    def filter(self, c, *_):
        asn, vrf, af = c
        return vrf != VRF_GLOBAL


# this abstract class and the two that follow are used to create two
# versions of each command class below by inheriting from each
# separately - one for the global VRF and one for a different VRF
#
# this class modifies the path during construction in two different
# ways by calling the _init_path() method during construction

class _AbsCvt_RtrBGP_AF_Nbr(Context_RtrBGP_AF):
    def __init__(self):
        self._init_path()
        super().__init__()

    def _init_path(self):
        pass


# this class is for commands in the global VRF: the commands start with
# 'neighbor ...' but still operate in the [global] address-family
# context - as such, this just appends that to the 'cmd' attribute
#
# this is because commands in the global address-family do not add or
# delete entire neighbors (that's done at the 'router bgp' level), but
# just configured parameters about them

class _AbsCvt_RtrBGP_AF_global_Nbr(_AbsCvt_RtrBGP_AF_Nbr):
    def _init_path(self):
        self.cmd = ("neighbor", None) + self.cmd

    def filter(self, c, *_):
        asn, vrf, af = c
        return vrf == VRF_GLOBAL


# on the other hand, this class is for commands in the non-global VRF:
# here the neighbor commands operate in a context of that neighbor,
# underneath the address-family - the context is extended by suffixing
# 'neighbor ...' onto it
#
# this is because, in a non-global VRF, neighbors are separate from
# those at the global level and must be created and can also be removed
# by removing the context, with 'no neighbor ...', rather than the
# individual parameters

class _AbsCvt_RtrBGP_AF_vrf_Nbr(_AbsCvt_RtrBGP_AF_Nbr):
    context_offset = -1

    def _init_path(self):
        self.context = self.context + ("neighbor", None)

    def filter(self, c, *_):
        asn, vrf, af = c
        return vrf != VRF_GLOBAL


# this is the global VRF version of 'neighbor ... activate'

class Cvt_RtrBGP_AF_global_Nbr_Act(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "activate",
    block = "bgp-nbr-activate"

    def remove(self, old, c, nbr):
        return self.enter(*c) + ["  no neighbor %s activate" % nbr]

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + ["  neighbor %s activate" % nbr]


# this creates the non-global VRF version of 'neighbor ... activate'
#
# this pattern continues for all commands below that exist in both the
# global or non-global VRF

class Cvt_RtrBGP_AF_vrf_Nbr_Act(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_Act):

    pass


class Cvt_RtrBGP_AF_global_Nbr_AddPath(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "additional-paths",

    def _add_paths(self, p):
        return (
            ' '.join([a for a in [ "send", "receive", "disable" ] if a in p]))

    def remove(self, old, c, nbr):
        return self.enter(*c) + [
                   "  no neighbor %s additional-paths" % nbr]

    def truncate(self, old, rem, new, c, nbr):
        # we can't remove types of additional-path, only provide a
        # complete new list
        return self.update(old, None, new, c, nbr)

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [
                   "  neighbor %s additional-paths %s"
                       % (nbr, self._add_paths(new))]


class Cvt_RtrBGP_AF_global_Nbr_AdvAddPath(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "advertise-additional-paths", None

    def remove(self, old, c, nbr, adv):
        # we can just remove any type and don't need to give the number
        # when removing 'best n'
        return self.enter(*c) + [
                   "  no neighbor %s advertise additional-paths %s"
                       % (nbr, adv)]

    def update(self, old, upd, new, c, nbr, adv):
        return self.enter(*c) + [
                   "  neighbor %s advertise additional-paths %s"
                       % (nbr, ("best %d" % new) if adv == "best" else adv)]


# Cvt_RtrBGP_AF_vrf_Nbr_AdvAddPath
#
# does not exist - there is no non-global VRF version of this


class Cvt_RtrBGP_AF_global_Nbr_AlwAS(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "allowas-in",

    def truncate(self, old, rem, new, c, nbr):
        # if we're truncating, we must be removing the 'max'
        return self.enter(*c) + [
                   "  neighbor %s allowas-in" % nbr]

    def remove(self, old, c, nbr):
        # removing the entire command
        return self.enter(*c) + [
                   "  no neighbor %s allowas-in" % nbr]

    def update(self, old, upd, new, c, nbr):
        # either changing the 'max' or adding a plain form
        return self.enter(*c) + [
                   "  neighbor %s allowas-in%s"
                       % (nbr, (" %d" % new["max"]) if "max" in new else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_AlwAS(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_AlwAS):

    pass


# Cvt_RtrBGP_AF_global_Nbr_FallOver[_xxx]
#
# do not exist - there is no global VRF version of this (done at the
# 'router bgp' level)


class Cvt_RtrBGP_AF_vrf_Nbr_FallOver(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_Nbr_FallOver):

    pass


# the 'neighbor ... fall-over' commands are in a subcontext under the
# neighbor, which is tricky to handle as the context for neighbors in an
# address-family are dynamically computed, so we extend the context
# after that has been done, using the method _init_path()


class Context_RtrBGP_AF_vrf_Nbr_FallOver(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Context_RtrBGP_Nbr_FallOver):

    def _init_path(self):
        super()._init_path()
        self.context = self.context + Cvt_RtrBGP_Nbr_FallOver.cmd


class Cvt_RtrBGP_AF_vrf_Nbr_FallOver_BFD(
    Context_RtrBGP_AF_vrf_Nbr_FallOver, Cvt_RtrBGP_Nbr_FallOver_BFD):

    pass


class Cvt_RtrBGP_AF_vrf_Nbr_FallOver_Route(
    Context_RtrBGP_AF_vrf_Nbr_FallOver, Cvt_RtrBGP_Nbr_FallOver_Route):

    pass


class Cvt_RtrBGP_AF_global_Nbr_FltLst(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "filter-list", None

    def remove(self, old, c, nbr, dir_):
        return self.enter(*c) + [
                   "  no neighbor %s filter-list %d %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, c, nbr, dir_):
        return self.enter(*c) + [
                   "  neighbor %s filter-list %d %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_vrf_Nbr_FltLst(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_FltLst):

    pass


class Cvt_RtrBGP_AF_global_Nbr_MaxPfx(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "maximum-prefix",

    def remove(self, old, c, nbr):
        # oddly, when removing, the old maximum must be spefified but
        # not the threshold
        return self.enter(*c) + [
                   "  no neighbor %s maximum-prefix %d" % (nbr, old["max"])]

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [
                   "  neighbor %s maximum-prefix %d%s"
                       % (nbr,
                          new["max"],
                          (" %d" % new["threshold"]) if "threshold" in new
                               else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_MaxPfx(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_MaxPfx):

    pass


class Cvt_RtrBGP_AF_global_Nbr_NHSelf(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "next-hop-self",

    def truncate(self, old, rem, new, c, nbr):
        # if we're truncating, we must be changing to the plain form
        return self.enter(*c) + [
                   "  neighbor %s next-hop-self" % nbr]

    def remove(self, old, c, nbr):
        # removing the entire command
        return self.enter(*c) + [
                   "  no neighbor %s next-hop-self" % nbr]

    def update(self, old, upd, new, c, nbr):
        # either updatring to 'all' or adding a plain form
        return self.enter(*c) + [
                   "  neighbor %s next-hop-self%s"
                       % (nbr, " all" if new.get("all") else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_NHSelf(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_NHSelf):

    pass


# Cvt_RtrBGP_AF_global_Nbr_Pwd
#
# does not exist - there is no global VRF version of this (done at the
# 'router bgp' level)


class Cvt_RtrBGP_AF_vrf_Nbr_Pwd(_AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_Nbr_Pwd):
    pass


# Cvt_RtrBGP_AF_global_Nbr_PrGrpMbr
#
# does not exist - there is no global VRF version of this (done at the
# 'router bgp' level)


class Cvt_RtrBGP_AF_vrf_Nbr_PrGrpMbr(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_Nbr_PrGrpMbr):

    pass


class Cvt_RtrBGP_AF_global_Nbr_PfxLst(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "prefix-list", None

    def remove(self, old, c, nbr, dir_):
        return self.enter(*c) + [
                   "  no neighbor %s prefix-list %s %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, c, nbr, dir_):
        return self.enter(*c) + [
                   "  neighbor %s prefix-list %s %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_vrf_Nbr_PfxLst(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_PfxLst):

    pass


class Cvt_RtrBGP_AF_vrf_Nbr_RemAS(_AbsCvt_RtrBGP_AF_vrf_Nbr):
    cmd = "remote-as",
    sort_key = "0_remote-as",

    def remove(self, old, c, nbr):
        return self.enter(*c) + [
                   "  no neighbor %s remote-as" % nbr]

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [
                   "  neighbor %s remote-as %s" % (nbr, new)]


class Cvt_RtrBGP_AF_global_Nbr_RemPrivAS(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "remove-private-as",

    def truncate(self, old, rem, new, c, nbr):
        # if we're truncating, we must be changing to the plain form
        return self.enter(*c) + [
                   "  neighbor %s remove-private-as" % nbr]

    def remove(self, old, c, nbr):
        # removing the entire command requires that 'all' is specified,
        # if it is enabled, otherwise nothing will be removed
        return self.enter(*c) + [
                   "  no neighbor %s remove-private-as%s"
                       % (nbr, " all" if old.get("all") else "")]

    def update(self, old, upd, new, c, nbr):
        # either updatring to 'all' or adding a plain form
        return self.enter(*c) + [
                   "  neighbor %s remove-private-as%s"
                       % (nbr, " all" if new.get("all") else "")]


class Cvt_RtrBGP_AF_vrf_Nbr_RemPrivAS(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_RemPrivAS):

    pass


class Cvt_RtrBGP_AF_global_Nbr_RtMap(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "route-map", None

    def remove(self, old, c, nbr, dir_):
        return self.enter(*c) + [
                   "  no neighbor %s route-map %s %s" % (nbr, old, dir_)]

    def update(self, old, upd, new, c, nbr, dir_):
        return self.enter(*c) + [
                   "  neighbor %s route-map %s %s" % (nbr, new, dir_)]


class Cvt_RtrBGP_AF_vrf_Nbr_RtMap(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_RtMap):

    pass


class Cvt_RtrBGP_AF_global_Nbr_SndCmty(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "send-community", None

    # the 'neighbor ... send-community' command is odd in that the
    # 'standard', 'extended' and 'both' options don't replace the
    # current setting but add or remove those communities to it
    #
    # the configuration is expressed as a set containing none, one or
    # both of 'standard' and 'extended'

    def remove(self, old, c, nbr, cmty):
       return self.enter(*c) + [
                   "  no neighbor %s send-community %s" % (nbr, cmty)]

    def update(self, old, upd, new, c, nbr, cmty):
        return self.enter(*c) + [
                   "  neighbor %s send-community %s" % (nbr, cmty)]


class Cvt_RtrBGP_AF_vrf_Nbr_SndCmty(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_SndCmty):

    pass


class Cvt_RtrBGP_AF_global_Nbr_SoftRecfg(_AbsCvt_RtrBGP_AF_global_Nbr):
    cmd = "soft-reconfiguration",

    def remove(self, old, c, nbr):
        return self.enter(*c) + [
                   "  no neighbor %s soft-reconfiguration %s" % (nbr, old)]

    def update(self, old, upd, new, c, nbr):
        return self.enter(*c) + [
                   "  neighbor %s soft-reconfiguration %s" % (nbr, new)]


class Cvt_RtrBGP_AF_vrf_Nbr_SoftRecfg(
    _AbsCvt_RtrBGP_AF_vrf_Nbr, Cvt_RtrBGP_AF_global_Nbr_SoftRecfg):

    pass
