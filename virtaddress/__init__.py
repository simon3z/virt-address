#
# Copyright 2015 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

from xml.dom.minidom import parseString
import libvirt

ARP_PATH = '/proc/net/arp'
ATF_COM = 0x02  # if_arp.h


class NetArp(object):
    def __init__(self, ip_address, hw_type, flags, hw_address,
                 mask, device):
        self.ip_address = ip_address
        self.hw_type = int(hw_type, 16)
        self.flags = int(flags, 16)
        self.hw_address = hw_address
        self.mask = mask
        self.device = device


def _get_net_arp_addresses(hw_addesses):
    with open(ARP_PATH, 'r') as f:
        f.readline()  # header line
        entries = (NetArp(*x.split()) for x in f.read().splitlines())

    def _address_filter(x):
        return (x.flags & ATF_COM) and (x.hw_address in hw_addesses)

    return filter(_address_filter, entries)


def _get_vm_mac_addresses(name, network=None):
    domain = libvirt.open().lookupByName(name)
    xmldesc = parseString(domain.XMLDesc(0))

    def _check_network(iface, network):
        for source in iface.getElementsByTagName('source'):
            if source.getAttribute('network') == network:
                return True
        return False

    address = []

    for iface in xmldesc.getElementsByTagName('interface'):
        if iface.getAttribute('type') != 'network':
            continue
        if network and not _check_network(iface, network):
            continue
        for mac in iface.getElementsByTagName('mac'):
            address.append(mac.getAttribute('address'))

    return address


def get_vm_arp(name, network=None):
    mac_addresses = _get_vm_mac_addresses(name, network)
    return _get_net_arp_addresses(mac_addresses)
