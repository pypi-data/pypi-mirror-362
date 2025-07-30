# asimtote.ios.converters.router.ospf
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



from ....diff import Convert



# --- converter classes ---



# =============================================================================
# router ospf ...
# =============================================================================



class Cvt_RtrOSPF(Convert):
    cmd = "router", "ospf", None

    def remove(self, old, proc):
        return "no router ospf " + str(proc)

    def add(self, new, proc):
        return "router ospf " + str(proc)


class Context_RtrOSPF(Convert):
    context = Cvt_RtrOSPF.cmd

    def enter(self, proc):
        return ["router ospf " + str(proc)]


class Cvt_RtrOSPF_Id(Context_RtrOSPF):
    cmd = "id",

    def remove(self, old, c):
        return self.enter(*c) + [" no router-id"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" router-id " + new]


class Cvt_RtrOSPF_AreaNSSA(Context_RtrOSPF):
    cmd = "area", None, "nssa"

    def remove(self, old, c, area):
        return self.enter(*c) + [" no area %s nssa" % area]

    def truncate(self, old, upd, new, c, area):
        # if we're truncating, we're removing options and we do that by
        # just re-entering the command without them, same as update()
        return self.update(old, None, new, c, area)

    def update(self, old, upd, new, c, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(*c) + [" area %s nssa%s" % (area, s)]


# passive-interface configuration is slightly odd as the default mode is
# stored (assuming it's not the default) and then a list of exceptions
# is maintained and it can go either way


class Cvt_RtrOSPF_PasvInt_Dflt(Context_RtrOSPF):
    cmd = "passive-interface", "default"

    def remove(self, old, c):
        return self.enter(*c) + [" no passive-interface default"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" passive-interface default"]


# ... the exception interface lists must execute after changing the
# default mode, which they will do as 'default' comes before 'interface'
# and 'no-interface'

class Cvt_RtrOSPF_PasvInt_Int(Context_RtrOSPF):
    cmd = "passive-interface",
    ext = "interface", None

    def delete(self, old, rem, new, c, int_name):
        # if we're changing the default mode, the old list of exceptions
        # will be removed by that, so we don't need to do it
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(*c) + [" no passive-interface " + int_name]

    def update(self, old, upd, new, c, int_name):
        return self.enter(*c) + [" passive-interface " + int_name]


class Cvt_RtrOSPF_PasvInt_NoInt(Context_RtrOSPF):
    cmd = "passive-interface",
    ext = "no-interface", None

    def delete(self, old, rem, new, c, int_name):
        # if we're changing the default mode, the old list of exceptions
        # will be removed by that, so we don't need to do it
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(*c) + [" passive-interface " + int_name]

    def update(self, old, upd, new, c, int_name):
        return self.enter(*c) + [" no passive-interface " + int_name]



# =============================================================================
# router ospfv3 ...
# =============================================================================



class Cvt_RtrOSPFv3(Convert):
    cmd = "router", "ospfv3", None

    def remove(self, old, c, proc):
        return "no router ospfv3 " + str(proc)

    def add(self, new, c, proc):
        return "router ospfv3 " + str(proc)


class Context_RtrOSPFv3(Convert):
    context = Cvt_RtrOSPFv3.cmd

    def enter(self, proc):
        return ["router ospfv3 " + str(proc)]


class Cvt_RtrOSPFv3_Id(Context_RtrOSPFv3):
    cmd = "id",

    def remove(self, old, c):
        return self.enter(*c) + [" no router-id"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" router-id " + new]


class Cvt_RtrOSPFv3_AreaNSSA(Context_RtrOSPFv3):
    cmd = "area", None, "nssa"

    def remove(self, old, c, area):
        return self.enter(*c) + [" no area %s nssa" % area]

    def truncate(self, old, upd, new, c, area):
        # if we're truncating, we're removing options and we do that by
        # just re-entering the command without them, same as update()
        return self.update(old, None, new, c, area)

    def update(self, old, upd, new, c, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(*c) + [" area %s nssa%s" % (area, s)]


class Cvt_RtrOSPFv3_AF(Context_RtrOSPFv3):
    cmd = "address-family", None

    def remove(self, old, c, af):
        return self.enter(*c) + [" no address-family " + af]

    def add(self, new, c, af):
        return self.enter(*c) + [" address-family " + af]


class Context_RtrOSPFv3_AF(Context_RtrOSPFv3):
    context = Context_RtrOSPFv3.context + Cvt_RtrOSPFv3_AF.cmd

    def enter(self, *c):
        c_super, (af, ) = c[:-1], c[-1:]
        return super().enter(*c_super) + [" address-family " + af]


# see the Cvt_RtrOSPF_... versions above for the explanation of how
# these converters work


class Cvt_RtrOSPFv3_AF_PasvInt_Dflt(Context_RtrOSPFv3_AF):
    cmd = "passive-interface", "default"

    def remove(self, old, c):
        return self.enter(*c) + [" no passive-interface default"]

    def update(self, old, upd, new, c):
        return self.enter(*c) + [" passive-interface default"]


class Cvt_RtrOSPFv3_AF_PasvInt_Int(Context_RtrOSPFv3_AF):
    cmd = "passive-interface",
    ext = "interface", None

    def delete(self, old, rem, new, c, int_name):
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(*c) + [" no passive-interface " + int_name]

    def update(self, old, upd, new, c, int_name):
        return self.enter(*c) + [" passive-interface " + int_name]


class Cvt_RtrOSPFv3_AF_PasvInt_NoInt(Context_RtrOSPFv3_AF):
    cmd = "passive-interface",
    ext = "no-interface", None

    def delete(self, old, rem, new, c, int_name):
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(*c) + [" passive-interface " + int_name]

    def update(self, old, upd, new, c, int_name):
        return self.enter(*c) + [" no passive-interface " + int_name]
