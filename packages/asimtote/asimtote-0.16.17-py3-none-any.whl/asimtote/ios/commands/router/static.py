# asimtote.ios.commands.router.static
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault
import netaddr

from ...utils import interface_canonicalize
from ....config import IndentedContextualCommand



# --- configuration command classes ---



# =============================================================================
# ip[v6] route ...
# =============================================================================



class Cmd_IPRoute(IndentedContextualCommand):
    match = (r"ip route( vrf (?P<vrf>\S+))? (?P<base>\S+) (?P<netmask>\S+)"
             r"( (?P<int_name>[-A-Za-z]+[0-9/.]+))?( (?P<router>[0-9.]+))?"
             r"( (?P<metric1>\d+))?( tag (?P<tag>\d+))?( (?P<metric2>\d+))?")

    def parse(self, cfg, vrf, base, netmask, int_name, router, metric1, tag,
              metric2):
        # get a canonical form of the destination network and interface name
        net = str(netaddr.IPNetwork(base + '/' + netmask))
        int_name = interface_canonicalize(int_name) if int_name else None

        # build a unique hashable indentifier for the next hop of this
        # route (i.e. interface and router address, if available)
        #
        # the actual contents are not important (although can be used in
        # a rule) but are needed to determine which routes are being
        # added, removed and changed (in terms of metric, tag, etc.) by
        # comparing the identifiers
        id = (int_name or '-') + ' ' + (router or '-')

        r = {}
        if int_name:
            r["interface"] = int_name
        if router:
            r["router"] = router
        if metric1 or metric2:
            r["metric"] = int(metric1 or metric2)
        if tag:
            r["tag"] = int(tag)

        deepsetdefault(cfg, "ip-route", vrf, net)[id] = r


class Cmd_IPv6Route(IndentedContextualCommand):
    match = (r"ipv6 route( vrf (?P<vrf>\S+))? (?P<net>\S+)"
             r"( (?P<int_name>[-A-Za-z]+[0-9/.]+))?( (?P<router>[0-9a-f:]+))?"
             r"( (?P<metric1>\d+))?( tag (?P<tag>\d+))?( (?P<metric2>\d+))?")

    def parse(self, cfg, vrf, net, int_name, router, metric1, tag, metric2):
        net = str(netaddr.IPNetwork(net))
        router = str(netaddr.IPAddress(router)) if router else None
        int_name = interface_canonicalize(int_name) if int_name else None

        id = (int_name or '-') + ' ' + (router or '-')

        r = {}
        if int_name:
            r["interface"] = int_name
        if router:
            r["router"] = router
        if metric1 or metric2:
            r["metric"] = int(metric1 or metric2)
        if tag:
            r["tag"] = int(tag)

        deepsetdefault(cfg, "ipv6-route", vrf, net)[id] = r
