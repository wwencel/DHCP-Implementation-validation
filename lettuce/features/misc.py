# Copyright (C) 2013 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#
# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#

from lettuce import *
from scapy.layers.dhcp6 import DHCP6OptOptReq

@step('Pass Criteria:')
def pass_criteria(step):
    # Do nothing, "Pass criteria:" appears in the text as beautification only
    pass

@step('Test Setup:')
def test_setup(step):
    # Do nothing, "Test Setup:" line is there as text bautification only
    if not hasattr(world, 'kea'):
        world.kea = {}
    else:
        world.kea.clear()
    world.kea["option_cnt"] = 0
    pass

@step('Test Procedure:')
def test_procedure(step):

    # Start with fresh, empty ORO (v6)
    if hasattr(world, 'oro'):
        world.oro = DHCP6OptOptReq()
        # Scapy creates ORO with 23, 24 options request. Let's get rid of them
        world.oro.reqopts = [] # don't request anything by default

    # Start with fresh, empty PRL (v4)
    if hasattr(world, 'prl'):
        world.prl = "" # don't request anything by default
