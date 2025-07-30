# asimtote.ios.commands.lists
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from deepops import deepsetdefault

from ..utils import ip_acl_ext_rule_canonicalize, ipv6_acl_rule_canonicalize
from ...config import IndentedContextualCommand



# --- configuration command classes ---



# =============================================================================
# ip access-list standard ...
# =============================================================================



class Cmd_ACLStdRule(IndentedContextualCommand):
    match = r"access-list (?P<num>\d{1,2}|1[3-9]\d{2}) (?P<rule>.+)"

    def parse(self, cfg, num, rule):
        # add this entry to the highest existing number +10, or 10 if
        # the list is currently empty / does not exist
        l = deepsetdefault(cfg, "ip-access-list-standard-seq", num)
        l[(max(l) + 10) if l else 10] = rule


class Cmd_IPACL_Std(IndentedContextualCommand):
    match = r"ip access-list standard (?P<acl_name>.+)"
    enter_context = "ip-acl_std"

    def parse(self, cfg, acl_name):
        return deepsetdefault(cfg, "ip-access-list-standard-seq", acl_name)


class Cmd_IPACL_Std_Rule(IndentedContextualCommand):
    context = "ip-acl_std"
    # standard ACLs can have multiple spaces after permit/deny
    match = r"((?P<seq>\d+) )?(?P<rule>(permit|deny) +.+)"

    def parse(self, cfg, seq, rule):
        # don't store the rule if one with the same sequence number
        # already exists (IOS would print an error, but we just ignore)
        if seq and (int(seq) in cfg):
            return

        # store the rule at the specified sequence number, or 10 greater
        # than the maximum existing rule number, or 10 if the list is
        # empty
        cfg[int(seq) if seq else ((max(cfg) + 10) if cfg else 10)] = rule



# =============================================================================
# ip access-list extended ...
# =============================================================================



class Cmd_ACLExtRule(IndentedContextualCommand):
    match = r"access-list (?P<num>1\d{2}|2[0-6]\d{2}) (?P<rule>(permit|deny) .+)"

    def parse(self, cfg, num, rule):
        l = deepsetdefault(cfg, "ip-access-list-extended-seq", num)
        l[(max(l) + 10) if l else 10] = ip_acl_ext_rule_canonicalize(rule)


class Cmd_IPACL_Ext(IndentedContextualCommand):
    match = r"ip access-list extended (?P<name>.+)"
    enter_context = "ip-acl_ext"

    def parse(self, cfg, name):
        return deepsetdefault(cfg, "ip-access-list-extended-seq", name)


class Cmd_IPACL_Ext_Rule(IndentedContextualCommand):
    context = "ip-acl_ext"
    match = r"((?P<seq>\d+) )?(?P<rule>(permit|deny) .+)"

    def parse(self, cfg, seq, rule):
        if seq and (int(seq) in cfg):
            return

        cfg[int(seq) if seq else ((max(cfg) + 10) if cfg else 10)] = (
            ip_acl_ext_rule_canonicalize(rule))



# =============================================================================
# ipv6 access-list ...
# =============================================================================



class Cmd_IPv6ACL(IndentedContextualCommand):
    match = r"ipv6 access-list (?P<name>.+)"
    enter_context = "ipv6-acl"

    def parse(self, cfg, name):
        return deepsetdefault(cfg, "ipv6-access-list-seq", name)


class Cmd_IPv6ACL_Rule(IndentedContextualCommand):
    context = "ipv6-acl"
    match = r"(sequence (?P<seq>\d+) )?(?P<rule>(permit|deny) +.+)"

    def parse(self, cfg, seq, rule):
        # unlike prefix-lists and IPv4 access-lists, entering a rule
        # with the same sequence number as an existing rule will replace
        # it, rather than produce an error
        cfg[int(seq) if seq else ((max(cfg) + 10) if cfg else 10)] = (
            ipv6_acl_rule_canonicalize(rule))



# =============================================================================
# ip as-path access-list ...
# =============================================================================



class Cmd_IPASPathACL(IndentedContextualCommand):
    match = (r"ip as-path access-list (?P<num>\d+) (?P<action>permit|deny)"
             r" (?P<re>\S+)")

    def parse(self, cfg, num, action, re):
        # an AS path access-list is just a sequence of tuples giving the
        # action and the regexp
        l = deepsetdefault(cfg, "ip-as-path-access-list", int(num), last=[])
        l.append( (action, re) )



# =============================================================================
# ip[v6] prefix-list ...
# =============================================================================



class Cmd_IPPfxList(IndentedContextualCommand):
    match = (r"ip prefix-list (?P<list_>\S+)( seq (?P<seq>\d+))? "
             r"(?P<rule>(permit|deny) .+)")

    def parse(self, cfg, list_, seq, rule):
        l = deepsetdefault(cfg, "ip-prefix-list-seq", list_)

        # don't store the rule if one with the same sequence number
        # already exists (IOS would print an error if the rule differed,
        # but we just ignore)
        if seq and (int(seq) in l):
            return

        # store the supplied sequence number, or 5 greater than the
        # highest existing number, or 5 if the list is empty
        # TODO: parse into data structure
        l[int(seq) if seq else ((max(l) + 5) if l else 5)] = rule


class Cmd_IPv6PfxList(IndentedContextualCommand):
    match = (r"ipv6 prefix-list (?P<list_>\S+)( seq (?P<seq>\d+))? "
             r"(?P<rule>(permit|deny) .+)")

    def parse(self, cfg, list_, seq, rule):
        l = deepsetdefault(cfg, "ipv6-prefix-list-seq", list_)
        if seq and (int(seq) in l):
            return
        # TODO: for now, we lower-case the rule to get the IPv6
        # address format canonical, but we really should parse the rule
        # fields into a data structure
        l[int(seq) if seq else ((max(l) + 5) if l else 5)] = rule.lower()
