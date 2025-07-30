# asimtote.ios.converters.interface
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from ..utils import is_int_physical

from ...diff import Convert



# --- converter classes ---



class Cvt_Int(Convert):
    cmd = "interface", None

    def remove(self, old, c, int_name):
         # if the interface is physical, we can't delete it ...
        if is_int_physical(int_name):
            # ... but, if there was something in the old configuration
            # other than just it being shut down, we 'default' it
            if old.keys() != { "shutdown" }:
                return "default interface " + int_name

            # the only thing in the old configuration was that it was
            # shutdown, so we ignore this
            return

        return "no interface " + int_name

    def add(self, new, c, int_name):
        # physical interfaces don't need creating (it doesn't hurt but
        # it's not necessary and makes the unit tests more cumbersome)
        if not is_int_physical(int_name):
            return "interface " + int_name


class Context_Int(Convert):
    context = Cvt_Int.cmd

    def enter(self, int_name):
        return ["interface " + int_name]



# =============================================================================
# shutdown
# =============================================================================



# we put the 'interface / shutdown' at the start to shut it down before
# we do any [re]configuration

class Cvt_Int_Shutdown(Context_Int):
    cmd = "shutdown",
    block = "int-shutdown"

    def update(self, old, upd, new, c):
        # we only 'shutdown' if we are disabling the port ('no shutdown'
        # happens at the end of interface configuration)
        if new:
            return self.enter(*c) + [" shutdown"]



# =============================================================================
# ...
# =============================================================================



# converter to detect a VRF change and fire a trigger to make changes
# required before it is actually changed

class Cvt_VRFTrgr_VRFFwd(Context_Int):
    cmd = "vrf-forwarding",
    block = "int-vrf-trigger"
    trigger_blocks = { "int-vrf-pre" }
    empty_trigger = True


# we do VRF changes on an interface before we do any IP address
# configuration, otherwise the IP configuration will be removed

class Cvt_Int_VRFFwd(Context_Int):
    cmd = "vrf-forwarding",
    block = "int-vrf"
    trigger_blocks = { "int-vrf-post" }

    def remove(self, old, c):
        return self.enter(*c) + [" no vrf forwarding"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" vrf forwarding " + new]


class Cvt_Int_ARPTime(Context_Int):
    cmd = "arp-timeout",

    def remove(self, old, c):
        return self.enter(*c) + [" no arp timeout"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" arp timeout " + str(new)]


class Cvt_Int_BFDIntvl(Context_Int):
    cmd = "bfd-interval",

    def remove(self, old, c):
        return self.enter(*c) + [" no bfd interval"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" bfd interval %d min_rx %d multiplier %d"
                                     % (new["interval"], new["min-rx"],
                                        new["multiplier"])]


class Cvt_Int_CDPEna(Context_Int):
    cmd = "cdp-enable",

    def remove(self, old, c):
        # if the 'cdp enable' option is not present, that just means
        # it's reverted to the default setting of enabled - if it wasn't
        # previously enabled, we do that
        if not old:
            return self.enter(*c) + [" cdp enable"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [ ' ' + ("" if upd else "no ") + "cdp enable"]


class Cvt_Int_ChnGrp(Context_Int):
    cmd = "channel-group",

    def remove(self, old, c):
        return self.enter(*c) + [" no channel-group"]

    def update(self, old, upd, new, c):
        id_, mode = new
        return self.enter(*c) + [
                   " channel-group %d%s" % (id_, mode if mode else "")]


class Cvt_Int_Desc(Context_Int):
    cmd = "description",

    def remove(self, old, c):
        return self.enter(*c) + [" no description"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" description " + new]


class Cvt_Int_Encap(Context_Int):
    cmd = "encapsulation",

    def remove(self, old, c):
        return self.enter(*c) + [" no encapsulation " + old]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" encapsulation " + new]


class Cvt_Int_FEC(Context_Int):
    cmd = "fec",

    def remove(self, old, c):
        return self.enter(*c) + [" no fec"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" fec " + new]


class Cvt_Int_IPAccGrp(Context_Int):
    cmd = "ip-access-group", None

    def remove(self, old, c, dir_):
        return self.enter(*c) + [" no ip access-group " + dir_]

    def update(self, old, upd, new, c, dir_):
        return self.enter(*c) + [" ip access-group %s %s" % (new, dir_)]



# =============================================================================
# ip address ...
# =============================================================================



class Cvt_Int_IPAddr(Context_Int):
    cmd = "ip-address",
    block = "int-vrf-post"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip address"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip address " + new]


class Cvt_Int_IPAddrSec(Context_Int):
    cmd = "ip-address-secondary", None
    block = "int-vrf-post"

    def remove(self, old, c, addr):
        return self.enter(*c) + [" no ip address %s secondary" % addr]

    def update(self, old, upd, new, c, addr):
        return self.enter(*c) + [" ip address %s secondary" % addr]



# =============================================================================
# ...
# =============================================================================



class Cvt_Int_IPFlowMon(Context_Int):
    cmd = "ip-flow-monitor", None

    def remove(self, old, c, dir_):
        return self.enter(*c) + [" no ip flow monitor %s %s" % (old, dir_)]

    def update(self, old, upd, new, c, dir_):
        l = self.enter(*c)

        # we must remove the old flow monitor before setting a new one
        if old:
            l += [" no ip flow monitor %s %s" % (old, dir_)]

        l += [" ip flow monitor %s %s" % (new, dir_)]
        return l



# =============================================================================
# ip helper-address ...
# =============================================================================



# This command is odd in that changing VRF causes it to be modified but
# not removed (as configuration items mentioning IP addresses are).  For
# example, if the interface is not in a VRF but is being moved into one,
# the VRF change will cause it to change to 'ip helper-address global
# ADDR'; removing it from a VRF change it to 'ip helper-address vrf
# VRF-NAME ADDR'.
#
# To handle this, we remove the helper address before the VRF change and
# then re-add it after changing it.  This is achieved through blocks and
# triggers.


class _AbsCvt_Int_IPHlprAddr(Context_Int):
    "Abstract class for 'ip helper-address'."

    cmd = "ip-helper-address", None

    def _cmd(self, helper):
        return ("ip helper-address"
                + (" global" if "global" in helper else "")
                + (" vrf " + helper["vrf"] if "vrf" in helper else "")
                + ' ' + helper["addr"])


class Cvt_VRFPre_IPHlprAddr(_AbsCvt_Int_IPHlprAddr):
    """Class to handle removing 'ip helper-address' commands prior to a
    VRF change.
    """

    block = "int-vrf-pre"

    def remove(self, old, c, helper):
        # if we're removing the helper address anyway, we just do that now
        return self.enter(*c) + [" no " + self._cmd(old)]

    def trigger(self, new, c, helper):
        # if we're not changing the helper address, we remove it prior
        # to changing VRF (to be re-added after the VRF change)
        return self.remove(new, c, helper)


class Cvt_VRFPost_Int_IPHlprAddr(_AbsCvt_Int_IPHlprAddr):
    """Class to handle adding (or re-adding, post a VRF change) 'ip
    helper-address' commands.
    """

    block = "int-vrf-post"

    # removing helper addresses is done before the VRF changes

    def update(self, old, upd, new, c, helper):
        return self.enter(*c) + [' ' + self._cmd(new)]



# =============================================================================
# ...
# =============================================================================



class Cvt_Int_IPIGMPVer(Context_Int):
    cmd = "ip-igmp-version",

    def remove(self, old, c):
        return self.enter(*c) + [" no ip igmp version"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip igmp version %d" % new]


class Cvt_Int_IPMcastBdry(Context_Int):
    cmd = "ip-multicast-boundary",

    def remove(self, old, c):
        return self.enter(*c) + [" no ip multicast boundary"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip multicast boundary " + new]



# =============================================================================
# ip ospf ...
# =============================================================================



class Cvt_Int_IPOSPFArea(Context_Int):
    cmd = "ip-ospf", "area"

    def remove(self, old, c):
        return self.enter(*c) + [
                   " no ip ospf %d area %s" % (old["process"], old["id"])]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [
                   " ip ospf %d area %s" % (new["process"], new["id"])]


class Cvt_Int_IPOSPFAuth(Context_Int):
    cmd = "ip-ospf", "authentication"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip ospf authentication"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip ospf authentication " + new]


class Cvt_Int_IPOSPFCost(Context_Int):
    cmd = "ip-ospf", "cost"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip ospf cost"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip ospf cost " + str(new)]


class Cvt_Int_IPOSPFDeadIvl(Context_Int):
    cmd = "ip-ospf", "dead-interval"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip ospf dead-interval"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip ospf dead-interval " + str(new)]


class Cvt_Int_IPOSPFHelloIvl(Context_Int):
    cmd = "ip-ospf", "hello-interval"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip ospf hello-interval"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip ospf hello-interval " + str(new)]


class Cvt_Int_IPOSPFMsgDigKey(Context_Int):
    cmd = "ip-ospf", "message-digest-key", None

    def remove(self, old, c, id_):
        return self.enter(*c) + [
                   " no ip ospf message-digest-key " + str(id_)]

    def update(self, old, upd, new, c, id_):
        return self.enter(*c) + [
                   " ip ospf message-digest-key %d md5 %s" % (id_, new)]


class Cvt_Int_IPOSPFNet(Context_Int):
    cmd = "ip-ospf", "network"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip ospf network"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip ospf network " + new]



# =============================================================================
# ip pim ...
# =============================================================================



class Cvt_Int_IPPIMMode(Context_Int):
    cmd = "ip-pim", "mode"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip pim %s-mode" % old]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip pim %s-mode" % new]


class Cvt_Int_IPPIMBSRBdr(Context_Int):
    cmd = "ip-pim", "bsr-border"
    block = "int-vrf-post"

    def remove(self, old, c):
        return self.enter(*c) + [" no ip pim bsr-border"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip pim bsr-border"]



# =============================================================================
# ip (other) ...
# =============================================================================



class Cvt_Int_IPPolicyRtMap(Context_Int):
    cmd = "ip-policy-route-map",

    def remove(self, old, c):
        return self.enter(*c) + [" no ip policy route-map"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip policy route-map " + new]


class Cvt_Int_IPProxyARP(Context_Int):
    cmd = "ip-proxy-arp",

    def remove(self, old, c):
        # if proxy ARP was disabled and we remove it, we're reverting to
        # the default of enabled
        if not old:
            return self.enter(*c) + [" ip proxy-arp"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [
                   ' ' + ("" if new else "no ") + "ip proxy-arp"]


class Cvt_Int_IPVerifyUni(Context_Int):
    cmd = "ip-verify-unicast",

    def remove(self, old, c):
        return self.enter(*c) + [" no ip verify unicast"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ip verify unicast " + new]



# =============================================================================
# ipv6 ...
# =============================================================================



class Cvt_Int_IPv6Addr(Context_Int):
    cmd = "ipv6-address", None
    block = "int-vrf-post"

    def remove(self, old, c, addr):
        return self.enter(*c) + [" no ipv6 address " + addr]

    def update(self, old, upd, new, c, addr):
        return self.enter(*c) + [" ipv6 address " + addr]


class Cvt_Int_IPv6MultBdry(Context_Int):
    cmd = "ipv6-multicast-boundary-scope",

    def remove(self, old, c):
        return self.enter(*c) + [" no ipv6 multicast boundary scope"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [ " ipv6 multicast boundary scope %d" % new]


class Cvt_Int_IPv6NDPfx(Context_Int):
    cmd = "ipv6-nd-prefix", None
    block = "int-vrf-post"

    def remove(self, old, c, pfx):
        return self.enter(*c) + [" no ipv6 nd prefix " + pfx]

    def update(self, old, upd, new, c, pfx):
        if "valid-lifetime" in new:
            # we're using relative number of seconds
            e = "%d %d" % (new["valid-lifetime"], new["preferred-lifetime"])
        else:
            # we're using absolute 'until' date/time
            e = "at %s %s" % (new["valid-until"], new["preferred-until"])
        return self.enter(*c) + [" ipv6 nd prefix %s %s" % (pfx, e)]


class Cvt_Int_IPv6PIMBSRBdr(Context_Int):
    cmd = "ipv6-pim", "bsr-border"
    block = "int-vrf-post"

    def remove(self, old, c):
        return self.enter(*c) + [" no ipv6 pim bsr border"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ipv6 pim bsr border"]


class Cvt_Int_IPv6PolicyRtMap(Context_Int):
    cmd = "ipv6-policy-route-map",

    def remove(self, old, c):
        return self.enter(*c) + [" no ipv6 policy route-map"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ipv6 policy route-map " + new]


class Cvt_Int_IPv6TrafFilt(Context_Int):
    cmd = "ipv6-traffic-filter", None

    def remove(self, old, c, dir_):
        return self.enter(*c) + [" no ipv6 traffic-filter " + dir_]

    def update(self, old, upd, new, c, dir_):
        return self.enter(*c) + [ " ipv6 traffic-filter %s %s" % (new, dir_)]


class Cvt_Int_IPv6VerifyUni(Context_Int):
    cmd = "ipv6-verify-unicast",

    def remove(self, old, c):
        return self.enter(*c) + [" no ipv6 verify unicast"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ipv6 verify unicast " + new]



# =============================================================================
# mpls ...
# =============================================================================



class Cvt_Int_MPLSIP(Context_Int):
    cmd = "mpls-ip",

    def remove(self, old, c):
        return self.enter(*c) + [" no mpls ip"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" mpls ip"]



# =============================================================================
# mtu ...
# =============================================================================



class Cvt_Int_MTU(Context_Int):
    cmd = tuple()
    ext = "mtu",

    def remove(self, old, c):
        # if interface is in a port-channel, the MTU is set in the
        # port-channel interface
        if "channel-group" in old:
            return None

        return self.enter(*c) + [" no mtu"]

    def update(self, old, upd, new, c):
        # TODO: handle what happens if interface converting to channel-group
        if new and "channel-group" in new:
            return None

        return self.enter(*c) + [" mtu " + str(self.get_ext(new))]



# =============================================================================
# ospfv3 ...
# =============================================================================



class Cvt_Int_OSPFv3Area(Context_Int):
    cmd = "ospfv3", "area", None

    def remove(self, old, c, proto):
        return self.enter(*c) + [
                   " no ospfv3 %d %s area %s"
                       % (old["process"], proto, old["id"])]

    def update(self, old, upd, new, c, proto):
        return self.enter(*c) + [
                   " ospfv3 %d %s area %s"
                       % (new["process"], proto, new["id"])]


class Cvt_Int_OSPFv3Cost(Context_Int):
    cmd = "ospfv3", "cost"

    def remove(self, old, c):
        return self.enter(*c) + [" no ospfv3 cost"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ospfv3 cost " + str(new)]


class Cvt_Int_OSPFv3DeadIvl(Context_Int):
    cmd = "ospfv3", "dead-interval"

    def remove(self, old, c):
        return self.enter(*c) + [" no ospfv3 dead-interval"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ospfv3 dead-interval " + str(new)]


class Cvt_Int_OSPFv3HelloIvl(Context_Int):
    cmd = "ospfv3", "hello-interval"

    def remove(self, old, c):
        return self.enter(*c) + [" no ospfv3 hello-interval"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ospfv3 hello-interval " + str(new)]


class Cvt_Int_OSPFv3Net(Context_Int):
    cmd = "ospfv3", "network"

    def remove(self, old, c):
        return self.enter(*c) + [" no ospfv3 network"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" ospfv3 network " + new]



# =============================================================================
# ...
# =============================================================================



class Cvt_Int_ServPol(Context_Int):
    cmd = "service-policy", None, None

    def _cmd(self, type_, dir_, name):
        return ("service-policy"
                + ((" type " + type_) if type_ else "")
                + ' ' + dir_ + ' ' + name)

    def remove(self, old, c, dir_, type_):
        return self.enter(*c) + [" no " + self._cmd(type_, dir_, old)]

    def update(self, old, upd, new, c, dir_, type_):
        l = self.enter(*c)

        # we cannot just replace a service-policy: we need to remove the
        # old one first
        if old:
            l.append(" no " + self._cmd(type_, dir_, old))

        l.append(' ' + self._cmd(type_, dir_, new))

        return l



# =============================================================================
# standby ...
# =============================================================================



class Cvt_Int_NoStandbyIPSec(Context_Int):
    cmd = "standby", "group", None, "ip-secondary", None
    block = "int-vrf-pre"

    def remove(self, old, c, grp, addr):
        return self.enter(*c) + [
                   " no standby %d ip %s secondary" % (grp, addr)]


class Cvt_Int_StandbyIP(Context_Int):
    cmd = "standby", "group", None, "ip"
    block = "int-vrf-post"

    def remove(self, old, c, grp):
        return self.enter(*c) + [" no standby %d ip" % grp]

    def update(self, old, upd, new, c, grp):
        return self.enter(*c) + [" standby %d ip %s" % (grp, new)]


class Cvt_Int_StandbyIPSec(Context_Int):
    cmd = "standby", "group", None, "ip-secondary", None
    block = "int-vrf-post"

    def update(self, old, upd, new, c, grp, addr):
        return self.enter(*c) + [
                   " standby %d ip %s secondary" % (grp, addr)]


class Cvt_Int_StandbyIPv6(Context_Int):
    cmd = "standby", "group", None, "ipv6", None
    block = "int-vrf-post"

    def remove(self, old, c, grp, addr):
        return self.enter(*c) + [" no standby %d ipv6 %s" % (grp, addr)]

    def update(self, old, upd, new, c, grp, addr):
        return self.enter(*c) + [" standby %d ipv6 %s" % (grp, addr)]


class Cvt_Int_StandbyPreempt(Context_Int):
    cmd = "standby", "group", None, "preempt"

    def remove(self, old, c, grp):
        return self.enter(*c) + [" no standby %d preempt" % grp]

    def update(self, old, upd, new, c, grp):
        return self.enter(*c) + [" standby %d preempt" % grp]


class Cvt_Int_StandbyPri(Context_Int):
    cmd = "standby", "group", None, "priority"

    def remove(self, old, c, grp):
        return self.enter(*c) + [" no standby %d priority" % grp]

    def update(self, old, upd, new, c, grp):
        return self.enter(*c) + [" standby %d priority %d" % (grp, new)]


class Cvt_Int_StandbyTimers(Context_Int):
    cmd = "standby", "group", None, "timers"

    def remove(self, old, c, grp):
        return self.enter(*c) + [" no standby %d timers" % grp]

    def update(self, old, upd, new, c, grp):
        return self.enter(*c) + [" standby %d timers %s" % (grp, new)]


class Cvt_Int_StandbyTrk(Context_Int):
    cmd = "standby", "group", None, "track", None

    def remove(self, old, c, grp, obj):
        return self.enter(*c) + [" no standby %d track %s" % (grp, obj)]

    def update(self, old, upd, new, c, grp, obj):
        return self.enter(*c) + [
                   " standby %d track %s%s"
                       % (grp, obj, (' ' + new) if new else "")]


class Cvt_Int_StandbyVer(Context_Int):
    cmd = "standby", "version"
    block = "int-pre"

    def update(self, old, upd, new, c):
        # only set this here if we're switching to version >= 2 (so we
        # can potentially use any high-numbered groups)
        #
        # version 1 is the default so is effectively removing 'standby
        # version' in the Cvt_Int_NoStandbyVer class
        if new < 2:
            return
        return self.enter(*c) + [" standby version " + str(new)]


class Cvt_Int_NoStandbyVer(Context_Int):
    cmd = "standby", "version"
    block = "int-post"

    def remove(self, old, c):
        return self.enter(*c) + [" no standby version"]

    def update(self, old, upd, new, c):
        # only set this here if we're switching to version < 2 (so we
        # need to do it after removing all the high-numbered groups)
        if new >= 2:
            return
        return self.enter(*c) + [" standby version " + str(new)]



# =============================================================================
# ...
# =============================================================================



class Cvt_Int_StormCtrl(Context_Int):
    cmd = "storm-control", None

    def remove(self, old, c, traffic):
        return self.enter(*c) + [" no storm-control %s level" % traffic]

    def update(self, old, upd, new, c, traffic):
        return self.enter(*c) + [
                   " storm-control %s level %.2f" % (traffic, new)]



# =============================================================================
# switchport ...
# =============================================================================



class Cvt_Int_SwPort(Context_Int):
    cmd = "switchport",

    def remove(self, old, c):
        # if the 'switchport' option is not present, that doesn't mean
        # it's disabled but just that it's not specified, so we assume
        # the default is for it to be disabled
        #
        # TODO: this is the case for routers (which we're concerned
        # about here) but not switches: we'd probably need a separate
        # platform for this
        return self.enter(*c) + [" no switchport"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [
                   ' ' + ("" if upd else "no ") + "switchport"]


class Cvt_Int_SwPortMode(Context_Int):
    cmd = "switchport-mode",

    def remove(self, old, c):
        return self.enter(*c) + [" no switchport mode"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" switchport mode " + new]


class Cvt_Int_SwPortNoNeg(Context_Int):
    cmd = "switchport-nonegotiate",

    def remove(self, old, c):
        return self.enter(*c) + [" no switchport nonegotiate"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" switchport nonegotiate"]


class Cvt_Int_SwPortTrkNtv(Context_Int):
    # we just match the interface as we need to look inside it to see if
    # the interface is part of a channel group
    cmd = tuple()
    ext = "switchport-trunk-native",

    def remove(self, old, c):
        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in old:
            return None

        return self.enter(*c) + [" no switchport trunk native vlan"]

    def update(self, old, upd, new, c):
        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in new:
            return None

        return self.enter(*c) + [
                   " switchport trunk native vlan " + str(self.get_ext(new))]


class Cvt_Int_SwPortTrkAlw(Context_Int):
    # we just match the interface as we need to look inside it to see if
    # the interface is part of a channel group
    cmd = tuple()
    ext = "switchport-trunk-allow",

    def remove(self, old, c):
        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in old:
            return None

        # we're removing all commands allowing VLANs which is a special
        # case as this actually means 'allow all'
        return self.enter(*c) + [" no switchport trunk allowed vlan"]

    def truncate(self, old, rem, new, c):
        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in old:
            return None

        l = self.enter(*c)
        for tag in sorted(self.get_ext(rem)):
            l.append(" switchport trunk allowed vlan remove " + str(tag))
        return l

    def update(self, old, upd, new, c):
        # if this interface is in a port-channel, we do all changes
        # there, so skip this
        if "channel-group" in new:
            return None

        l = self.enter(*c)

        # if this list was not there before, all VLANs were allowed by
        # default so we need to reset the list to 'none' and then add
        # the ones which are specifically listed
        if not old:
            l.append(" switchport trunk allowed vlan none")

        for tag in sorted(self.get_ext(upd)):
            l.append(" switchport trunk allowed vlan add " + str(tag))

        return l



# =============================================================================
# ...
# =============================================================================



class Cvt_Int_PcMinLinks(Context_Int):
    cmd = "port-channel-min-links",

    def remove(self, old, c):
        return self.enter(*c) + [" no port-channel min-links"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" port-channel min-links " + str(new)]


class Cvt_Int_PcStandaloneDis(Context_Int):
    # TODO: this is disabled by default on routing platforms but enabled
    # by default on switching platforms and we can't detect this; we're
    # only concerned with routers here, though

    cmd = "standalone-disable",

    def remove(self, old, c):
        return (self.enter(*c)
                + [ ' ' + ("no " if old else "")
                        + "port-channel standalone-disable"])

    def update(self, old, upd, new, c):
        return (self.enter(*c)
                + [ ' ' + ("" if upd else "no ")
                        + "port-channel standalone-disable"])


class Cvt_Int_XConn(Context_Int):
    cmd = "xconnect",

    def remove(self, old, c):
        return self.enter(*c) + [" no xconnect"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" xconnect " + new]



# =============================================================================
# no shutdown
# =============================================================================



# we put the 'interface / no shutdown' at the end to only enable the
# interface once it's been correctly [re]configured

class Cvt_Int_NoShutdown(Context_Int):
    cmd = "shutdown",
    block = "int-noshutdown"

    def update(self, old, upd, new, c):
        # we only 'no shutdown' if we are enabling the port ('shutdown'
        # happens at the start of interface configuration)
        if not new:
            return self.enter(*c) + [" no shutdown"]
