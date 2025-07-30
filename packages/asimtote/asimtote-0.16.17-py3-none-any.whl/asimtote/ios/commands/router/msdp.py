# asimtote.ios.commands.router.msdp
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault

from ....config import IndentedContextualCommand



# --- configuration command classes ---



# =============================================================================
# ip msdp ...
# =============================================================================



class Cmd_IPMSDP_Peer(IndentedContextualCommand):
    match = (r"ip msdp peer (?P<peer>\S+)"
             r"( connect-source (?P<int_name>\S+))?"
             r"( remote-as (?P<asn>\d+(\.\d+)?))?")

    def parse(self, cfg, peer, int_name, asn):
        p = deepsetdefault(cfg, "ip-msdp", "peers", peer, "peering")

        if int_name:
            p["connect-source"] = int_name

        if asn:
            p["remote-as"] = asn


class Cmd_IPMSDP_Peer_SAFilter(IndentedContextualCommand):
    match = (r"ip msdp sa-filter (?P<dir_>in|out) (?P<peer>\S+)"
             r" list (?P<list_>\S+)")

    def parse(self, cfg, dir_, peer, list_):
        deepsetdefault(cfg, "ip-msdp", "peers", peer, "sa-filter")[dir_] = (
            list_)


class Cmd_IPMSDP_Peer_SALimit(IndentedContextualCommand):
    match = r"ip msdp sa-limit (?P<peer>\S+) (?P<count>\d+)"

    def parse(self, cfg, peer, count):
        deepsetdefault(cfg, "ip-msdp", "peers", peer)["sa-limit"] = int(count)
