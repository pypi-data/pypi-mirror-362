# asimtote.ios.converters.router.rtmap
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepget

from ....diff import Convert



# --- converter classes ---



# =============================================================================
# route-map ...
# =============================================================================



class Cvt_RtMap(Convert):
    cmd = "route-map", None
    block = "rtmap-del"

    def remove(self, old, c, rtmap_name):
        return "no route-map " + rtmap_name


class Context_RtMap(Convert):
    context = Cvt_RtMap.cmd


class Cvt_RtMap_Entry(Context_RtMap):
    cmd = None,
    block = "rtmap-del"

    def remove(self, old, c, seq):
        rtmap_name, = c
        return "no route-map %s %d" % (rtmap_name, seq)


class Cvt_RtMap_Entry_Action(Context_RtMap):
    cmd = None, "action"
    block = "rtmap-add"

    def update(self, old, upd, new, c, seq):
        rtmap_name, = c
        return "route-map %s %s %d" % (rtmap_name, new, seq)


class Context_RtMap_Entry(Context_RtMap):
    context = Context_RtMap.context + Cvt_RtMap_Entry.cmd

    # route-map entries require you to know the action type ('permit' or
    # 'deny') when modifying them, which are in the dictionary element
    # underneath, in our configuration model
    def enter(self, rtmap_name, seq, rtmap_dict):
        return ["route-map %s %s %d" % (rtmap_name, rtmap_dict["action"], seq)]


class Cvt_RtMap_MatchCmty_Exact_del(Context_RtMap_Entry):
    cmd = tuple()
    ext = "match", "community", "exact-match"
    block = "rtmap-del"
    trigger_blocks = { "rtmap-add-cmty" }

    # if removing the exact-match option, we need to clear the list and
    # recreate it without it
    def remove(self, old, c):
        if self.get_ext(old):
            l = self.enter(*c, old)
            l.append(" no match community")
            return l


class _AbsCvt_RtMap_MatchCmty(Context_RtMap_Entry):
    cmd = tuple()
    ext = "match", "community", "communities", None


class Cvt_RtMap_MatchCmty_del(_AbsCvt_RtMap_MatchCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, c, cmty):
        l = self.enter(*c, old)
        l.append(" no match community " + cmty)
        return l


class Cvt_RtMap_MatchCmty_add(_AbsCvt_RtMap_MatchCmty):
    block = "rtmap-add-cmty"

    def update(self, old, upd, new, c, cmty):
        # TODO: need to handle applying 'exact-match' when list is the
        # same; will rework these to use context_offset to see if that
        # makes it easier (as we need the action from a higher context
        # but would like to set a lower context)
        l = self.enter(*c, new)
        exact_match = deepget(new, "match", "community", "exact-match")
        l.append(" match community %s%s"
                     % (cmty, " exact-match" if exact_match else ""))
        return l

    def trigger(self, new, c, *args):
        return self.update(None, new, new, c, *args)


class _AbsCvt_RtMap_MatchIPAddr(Context_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-address"

class Cvt_RtMap_MatchIPAddr_del(_AbsCvt_RtMap_MatchIPAddr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, c):
        l = self.enter(*c, old)
        for addr in sorted(self.get_ext(rem)):
            l.append(" no match ip address " + addr)
        return l

class Cvt_RtMap_MatchIPAddr_add(_AbsCvt_RtMap_MatchIPAddr):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        l = self.enter(*c, new)
        for addr in sorted(self.get_ext(upd)):
            l.append(" match ip address " + addr)
        return l


class _AbsCvt_RtMap_MatchIPPfxLst(Context_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-prefix-list"

class Cvt_RtMap_MatchIPPfxLst_del(_AbsCvt_RtMap_MatchIPPfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, c):
        l = self.enter(*c, old)
        for pfx in sorted(self.get_ext(rem)):
            l.append(" no match ip address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPPfxLst_add(_AbsCvt_RtMap_MatchIPPfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        l = self.enter(*c, new)
        for pfx in sorted(self.get_ext(upd)):
            l.append(" match ip address prefix-list " + pfx)
        return l


class _AbsCvt_RtMap_MatchIPv6Addr(Context_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-address"

class Cvt_RtMap_MatchIPv6Addr_del(_AbsCvt_RtMap_MatchIPv6Addr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, c):
        l = self.enter(*c, old)
        for addr in sorted(self.get_ext(rem)):
            l.append(" no match ipv6 address " + addr)
        return l

class Cvt_RtMap_MatchIPv6Addr_add(_AbsCvt_RtMap_MatchIPv6Addr):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        l = self.enter(*c, new)
        for addr in sorted(self.get_ext(upd)):
            l.append(" match ipv6 address " + addr)
        return l


class _AbsCvt_RtMap_MatchIPv6PfxLst(Context_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-prefix-list"

class Cvt_RtMap_MatchIPv6PfxLst_del(_AbsCvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, c):
        l = self.enter(*c, old)
        for pfx in sorted(self.get_ext(rem)):
            l.append(" no match ipv6 address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPv6PfxLst_add(_AbsCvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        l = self.enter(*c, new)
        for pfx in sorted(self.get_ext(upd)):
            l.append(" match ipv6 address prefix-list " + pfx)
        return l


class _AbsCvt_RtMap_MatchTag(Context_RtMap_Entry):
    cmd = tuple()
    ext = "match", "tag"

class Cvt_RtMap_MatchTag_del(_AbsCvt_RtMap_MatchTag):
    block = "rtmap-del"

    def truncate(self, old, rem, new, c):
        l = self.enter(*c, old)
        for tag in sorted(self.get_ext(rem)):
            l.append(" no match tag " + str(tag))
        return l

class Cvt_RtMap_MatchTag_add(_AbsCvt_RtMap_MatchTag):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        l = self.enter(*c, new)
        for tag in sorted(self.get_ext(upd)):
            l.append(" match tag " + str(tag))
        return l


class _AbsCvt_RtMap_SetCmty(Context_RtMap_Entry):
    cmd = tuple()
    ext = "set", "community", "communities"

class Cvt_RtMap_SetCmty_del(_AbsCvt_RtMap_SetCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, c):
        l = self.enter(*c, old)
        for cmty in sorted(self.get_ext(rem)):
            l.append(" no set community " + cmty)
        return l

class Cvt_RtMap_SetCmty_add(_AbsCvt_RtMap_SetCmty):
    block = "rtmap-add"

    # TODO: need to handle case where list is the same but 'additive'
    # is only addition or removal
    def update(self, old, upd, new, c):
        l = self.enter(*c, new)
        for cmty in sorted(self.get_ext(upd)):
            l.append(" set community "
                     + cmty
                     + (" additive" if "additive" in new["set"]["community"]
                            else ""))
        return l


class _AbsCvt_RtMap_SetIPNxtHop(Context_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        vrf = None
        if "vrf" in nexthop:
            vrf = ("vrf " + nexthop["vrf"]) if nexthop["vrf"] else "global"

        return "set ip" + ((' ' + vrf) if vrf else "") + " next-hop " + addr

class Cvt_RtMap_SetIPNxtHop_del(_AbsCvt_RtMap_SetIPNxtHop):
    block = "rtmap-del"

    def remove(self, old, c):
        # we must remove all the 'set ip next-hop' commands individually
        l = self.enter(*c, old)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPNxtHop_add(_AbsCvt_RtMap_SetIPNxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(*c, new)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(' ' + self._cmd(new_nexthop))
        return l


class Cvt_RtMap_SetIPNxtHopVrfy(Context_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop-verify-availability"

    def remove(self, old, c):
        l = self.enter(*c, old)
        l.append(" no set ip next-hop verify-availability")
        return l

    def update(self, old, upd, new, c):
        l = self.enter(*c, new)
        l.append(" set ip next-hop verify-availability")
        return l


class _AbsCvt_RtMap_SetIPNxtHopVrfyTrk(Context_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop-verify-availability-track", None

    def _cmd(self, seq, nexthop):
        return ("set ip next-hop verify-availability %s %s track %d"
                     % (nexthop["addr"], seq, nexthop["track-obj"]))

class Cvt_RtMap_SetIPNxtHopVrfy_del(_AbsCvt_RtMap_SetIPNxtHopVrfyTrk):
    block = "rtmap-del"

    def remove(self, old, c, nexthop_seq):
        return self.enter(*c, old) + [
                   " no "
                       + self._cmd(nexthop_seq,
                                   self.get_ext(old, nexthop_seq))]

class Cvt_RtMap_SetIPNxtHopVrfy_add(_AbsCvt_RtMap_SetIPNxtHopVrfyTrk):
    block = "rtmap-add"

    def update(self, old, upd, new, c, nexthop_seq):
        # individual entries (ordered by sequence number) can be replaced but
        # the old entry must be removed first, before the new one added
        l = self.enter(*c, new)
        if old:
            l.append(" no "
                     + self._cmd(nexthop_seq, self.get_ext(old, nexthop_seq)))
        l.append(' ' + self._cmd(nexthop_seq, self.get_ext(new, nexthop_seq)))
        return l


class _AbsCvt_RtMap_SetIPv6NxtHop(Context_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ipv6-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        return "set ipv6 next-hop " + addr

class Cvt_RtMap_SetIPv6NxtHop_del(_AbsCvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-del"

    def remove(self, old, c):
        # we must remove all the 'set ipv6 next-hop' commands individually
        l = self.enter(*c, old)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPv6NxtHop_add(_AbsCvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(*c, new)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(' ' + self._cmd(new_nexthop))
        return l


class _AbsCvt_RtMap_SetLocalPref(Context_RtMap_Entry):
    cmd = tuple()
    ext = "set", "local-preference"

class Cvt_RtMap_SetLocalPref_del(_AbsCvt_RtMap_SetLocalPref):
    block = "rtmap-del"

    def remove(self, old, c):
        return self.enter(*c, old) + [" no set local-preference"]

class Cvt_RtMap_SetLocalPref_add(_AbsCvt_RtMap_SetLocalPref):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        return self.enter(*c, new) + [
                   " set local-preference " + str(self.get_ext(new))]


class _AbsCvt_RtMap_SetVRF(Context_RtMap_Entry):
    # this handles both 'set global' and 'set vrf ...'
    cmd = tuple()
    ext = "set", "vrf"

    def _cmd(self, entry):
        vrf = self.get_ext(entry)
        return "set " + (("vrf " + vrf) if vrf else "global")

class Cvt_RtMap_SetVRF_del(_AbsCvt_RtMap_SetVRF):
    block = "rtmap-del"

    def remove(self, old, c):
        return self.enter(*c, old) + [" no " + self._cmd(old)]

class Cvt_RtMap_SetVRF_add(_AbsCvt_RtMap_SetVRF):
    block = "rtmap-add"

    def update(self, old, upd, new, c):
        l = self.enter(*c, new)

        # if there's a previous setting, and we're changing from global
        # to a VRF, or vice-versa, we need to clear the old setting
        # first
        if old and (bool(self.get_ext(old)) != bool(self.get_ext(new))):
            l.append(" no " + self._cmd(old))

        l.append(' ' + self._cmd(new))
        return l
