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
import os
import sys
import random
import scapy
from scapy.sendrecv import send,sendp,sniff
from scapy.all import *
from scapy.layers.dhcp import *


#@step('Client requests option (\d+).')
def client_requests_option(step, opt_type):
    if not hasattr(world, 'prl'):
        world.prl = "" # don't request anything by default
    world.prl += chr(int(opt_type)) # put a single byte there

def client_send_msg(step, msgname, opt_type, unknown):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    num_opts: number of options to send.
    opt_type: option type
    """

    options = []

    if hasattr(world, 'prl'):
        options += [("param_req_list", str(world.prl))]
    else:
        assert False, "No PRL defined"

    options += ["end"] # end option

    if (msgname == "DISCOVER"):
        msg = create_discover(options)
    elif (msgname == "OFFER"):
        msg = create_offer()
    elif (msgname == "REQUEST"):
        msg = create_request()
    elif (msgname == "ACK"):
        msg = create_ack()
    elif (msgname == "NAK"):
        msg = create_nak()
    elif (msgname == "DHCPINFORM"):
        msg = create_inform()
    elif (msgname == "DHCPRELEASE"):
        msg = create_release()
    else:
        assert False, "Invalid message type: %s" % msgname

    assert msg, "Failed to create " + msgname

    if msg:
        world.climsg.append(msg)

    print("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))


def create_discover(options):

    opts = [("message-type","discover")]
    if options:
        opts += options
    else:
        assert False

    conf.checkIPaddr = False
    fam,hw = get_if_raw_hwaddr(conf.iface)

    discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src=world.cfg["rel4_addr"],dst=world.cfg["srv4_addr"])
    discover /= UDP(sport=68,dport=67)/BOOTP(chaddr=hw, giaddr="192.0.2.1")
    dhcp = DHCP(options=opts)
    discover /= dhcp
    return discover

# @step('Server MUST respond with (\w+) message')
def send_wait_for_message(step, message):
    """
    Block until the given message is (not) received.
    Parameter:
    new: (' new', optional): Only check the output printed since last time
                             this step was used for this process.
    process_name ('<name> stderr'): Name of the process to check the output of.
    message ('message <message>'): Output (part) to wait for.
    not_message ('not <message>'): Output (part) to wait for, and fail
    Fails if the message is not found after 10 seconds.
    """

    # We need to use srp() here (send and receive on layer 2)
    ans,unans = srp(world.climsg, iface=world.cfg["iface"], timeout=2, multi=True, verbose=1)

    world.srvmsg = []
    for x in ans:
        a,b = x
        world.srvmsg.append(b)

    print("Received traffic (answered/unanswered): %d/%d packet(s)." % (len(ans), len(unans)))

    assert len(world.srvmsg) != 0, "No response received."


# @step('Response MUST (NOT )?include option (\d+).')
def response_check_include_option(step, yes_or_no, opt_code):

    assert len(world.srvmsg) != 0, "No response received."

    opt = get_option(world.srvmsg[0], opt_code)

    assert opt, "Expected option " + opt_code + " not present in the message."


# Returns option of specified type
def get_option(msg, opt_code):
    # We need to iterate over all options and see
    # if there's one we're looking for
    
    opt_name = DHCPOptions[int(opt_code)]

    # dhcpv4 implementation in Scapy is a mess. The options array contains mix of 
    # strings, IPField, ByteEnumField and who knows what else. In each case the
    # values are accessed differenty
    if (isinstance(opt_name, Field)):
        opt_name = opt_name.name

    x = msg.getlayer(4) # 0th is Ethernet, 1 is IPv4, 2 is UDP, 3 is BOOTP, 4 is DHCP options
    for opt in x.options:
        if opt[0] == opt_name:
            return opt
    return None


# Option 23 MUST contain addresses 1.2.3.4, 5.6.7.8.
# @step('Response option (\d+) MUST (NOT )?contain (\S+) (\S+).')
def response_check_option_content(step, opt_code, expect, data_type, expected):

    opt_code = int(opt_code)

    assert len(world.srvmsg) != 0, "No response received."

    opt_name, received = get_option(world.srvmsg[0], opt_code)

    assert opt_name, "Expected option " + opt_code + " not present in the message."

    assert expected == received, "Invalid " + opt_code + " option received:" + received + \
                                 ", but expected " + expected
