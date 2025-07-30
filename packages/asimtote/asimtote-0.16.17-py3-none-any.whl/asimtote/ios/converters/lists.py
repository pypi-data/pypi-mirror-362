# asimtote.ios.converters.lists
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from ..utils import explain_diffs

from ...diff import Convert



# --- converter classes ---



# =============================================================================
# ip[v6] access-list ...
# =============================================================================



class Cvt_IPACL_Std(Convert):
    cmd = "ip-access-list-standard", None

    def remove(self, old, _, acl_name):
        return "no ip access-list standard " + acl_name

    def update(self, old, upd, new, _, acl_name):
        r = []
        if old:
            r.append("no ip access-list standard " + acl_name)
        r.append("ip access-list standard " + acl_name)
        r.extend(explain_diffs(old, new, indent=' '))
        return r


class Cvt_IPACL_Ext(Convert):
    cmd = "ip-access-list-extended", None

    def remove(self, old, _, acl_name):
        return "no ip access-list extended " + acl_name

    def update(self, old, upd, new, _, acl_name):
        r = []
        if old:
            r.append("no ip access-list extended " + acl_name)
        r.append("ip access-list extended " + acl_name)
        r.extend(explain_diffs(old, new, indent=' '))
        return r


class Cvt_IPv6ACL(Convert):
    cmd = "ipv6-access-list", None

    def remove(self, old, _, acl_name):
        return "no ipv6 access-list " + acl_name

    def update(self, old, upd, new, _, acl_name):
        r = []
        if old:
            r.append("no ipv6 access-list " + acl_name)
        r.append("ipv6 access-list " + acl_name)
        r.extend(explain_diffs(old, new, indent=' '))
        return r



# =============================================================================
# ip as-path access-list ...
# =============================================================================



class Cvt_IPASPathACL(Convert):
    cmd = "ip-as-path-access-list", None

    def to_str(self, rule):
        action, re = rule
        return action + ' ' + re

    def remove(self, old, _, num):
        return "no ip as-path access-list " + str(num)

    def update(self, old, upd, new, _, num):
        r = []
        if old:
            r += ["no ip as-path access-list " + str(num)]
        r += explain_diffs(old, new, prefix="ip as-path access-list %d " % num,
                           to_str_func=self.to_str)
        return r



# =============================================================================
# ip[v6] prefix-list ...
# =============================================================================



class Cvt_IPPfxList(Convert):
    cmd = "ip-prefix-list", None

    def remove(self, old, _, pfx_name):
        return "no ip prefix-list " + pfx_name

    def update(self, old, upd, new, _, pfx_name):
        r = []
        if old:
            r.append("no ip prefix-list " + pfx_name)
        r.extend(explain_diffs(
                     old, new, prefix="ip prefix-list %s " % pfx_name))
        return r


class Cvt_IPv6PfxList(Convert):
    cmd = "ipv6-prefix-list", None

    def remove(self, old, _, pfx_name):
        return "no ipv6 prefix-list " + pfx_name

    def update(self, old, upd, new, _, pfx_name):
        r = []
        if old:
            r.append("no ipv6 prefix-list " + pfx_name)
        r.extend(explain_diffs(
                     old, new, prefix="ipv6 prefix-list %s " % pfx_name))
        return r
