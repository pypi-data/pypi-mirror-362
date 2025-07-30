# asimtote.ios.converters.router.msdp
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from ....diff import Convert



# --- converter classes ---



# =============================================================================
# ip msdp ...
# =============================================================================



class Cvt_IPMSDP_Peer(Convert):
    cmd = "ip-msdp", "peers", None
    ext = "peering",

    def _cmd(self, peer):
        return "ip msdp peer " + peer

    def remove(self, old, c, peer):
        return "no " + self._cmd(peer)

    def update(self, old, upd, new, c, peer):
        m = self._cmd(peer)
        if "peering" in new:
            p = new["peering"]
            if "connect-source" in p:
                m += " connect-source " + p["connect-source"]
            if "remote-as" in p:
                m += " remote-as " + p["remote-as"]
        return m


class Context_IPMSDP_Peer(Convert):
    context = Cvt_IPMSDP_Peer.cmd


class Cvt_IPMSDP_Peer_SAFilter(Context_IPMSDP_Peer):
    cmd = "sa-filter", None

    def _cmd(self, peer, dir_):
        return "ip msdp sa-filter " + dir_ + " " + peer

    def remove(self, old, c, dir_):
        return "no " + self._cmd(*c, dir_)

    def update(self, old, upd, new, c, dir_):
        return self._cmd(*c, dir_) + " list " + new


class Cvt_IPMSDP_Peer_SALimit(Context_IPMSDP_Peer):
    cmd = "sa-limit",

    def _cmd(self, peer):
        return "ip msdp sa-limit " + peer

    def remove(self, old, c):
        return "no " + self._cmd(*c)

    def update(self, old, upd, new, c):
        return self._cmd(*c) + " " + str(new)
