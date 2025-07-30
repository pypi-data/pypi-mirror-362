# asimtote.ios.converters.__init__
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration converters module.

This module contains the converters to change individual configuration
elements of a Cisco IOS configuration into another.
"""



from .interface import *
from .lists import *
from .other import *
from .router import *

from ...misc import get_all_subclasses



# the converters are all subclasses of Convert which have the 'cmd'
# attribute defined, stored as a set - the order is not important as we
# sort the list later
#
# CiscoIOSDiffConfig._add_converters() adds these into the list of
# converter classes

converters = {
    c for c in get_all_subclasses(Convert) if c.cmd is not None  }
