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

import argparse
import libvirt
import sys

from . import get_vm_arp

CLI_ARGUMENTS = (
    (('--domain', '-d'), {
        'help': 'domain name',
        'required': True,
    }),
    (('--network', '-n'), {
        'default': None,
        'help': 'virtual network name',
    }),
)


def fatal_error(message, code=1):
    sys.stderr.write('error: {0}\n'.format(message))
    sys.exit(code)


def main():
    parser = argparse.ArgumentParser()

    for args, kwargs in CLI_ARGUMENTS:
        parser.add_argument(*args, **kwargs)

    args = parser.parse_args()
    libvirt.registerErrorHandler(lambda x, y: None, None)

    try:
        net_arp = get_vm_arp(args.domain, network=args.network)
    except libvirt.libvirtError as e:
        fatal_error(e.get_error_message())

    print "\n".join((x.ip_address for x in net_arp))
