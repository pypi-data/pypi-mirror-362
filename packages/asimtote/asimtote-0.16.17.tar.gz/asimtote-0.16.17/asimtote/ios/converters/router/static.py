# asimtote.ios.converters.router.static
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



import netaddr

from ....diff import Convert



# --- converter classes ---



# =============================================================================
# ip[v6] route ...
# =============================================================================



class Cvt_IPRoute(Convert):
    cmd = "ip-route", None, None, None

    def _cmd(self, vrf, net, r):
        n = netaddr.IPNetwork(net)

        return ("ip route"
                + ((" vrf " + vrf) if vrf else "")
                + ' ' + str(n.network) + ' ' + str(n.netmask)
                + ((' ' + r["interface"]) if "interface" in r else "")
                + ((' ' + r["router"]) if "router" in r else "")
                + ((" %d" % r["metric"]) if "metric" in r else "")
                + ((" tag %d" % r["tag"]) if "tag" in r else ""))

    def remove(self, old, c, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, c, vrf, net, id):
        return self._cmd(vrf, net, new)


class Cvt_IPv6Route(Convert):
    cmd = "ipv6-route", None, None, None

    def _cmd(self, vrf, net, r):
        return ("ipv6 route"
                + ((" vrf " + vrf) if vrf else "")
                + ' ' + net
                + ((' ' + r["interface"]) if "interface" in r else "")
                + ((' ' + r["router"]) if "router" in r else "")
                + ((' ' + str(r["metric"])) if "metric" in r else "")
                + ((" tag " + str(r["tag"])) if "tag" in r else ""))

    def remove(self, old, c, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, c, vrf, net, id):
        return self._cmd(vrf, net, new)
