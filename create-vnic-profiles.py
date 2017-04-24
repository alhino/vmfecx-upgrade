#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import ast
import getpass
import logging
import sys

from ovirtsdk.api import API
from ovirtsdk.xml import params

logging.basicConfig(level=logging.DEBUG, filename='vmfex-upgrade.log')
logging.getLogger().addHandler(logging.StreamHandler())

def create_vnic(api, dcname, profiles, net):
    dc = api.datacenters.get(dcname)
    network = next(
        (
            n for n in dc.networks.list()
            if n.get_name() == net
        ),
        None
    )
    if not network:
        logging.error("Couldn't find network: '%s' in dc: '%s'", net, dc.get_name())
        return False

    for profile_name in profiles.split(','):
        profile = next(
            (
                p for p in api.vnicprofiles.list()
                if p.get_network().get_id() == network.get_id() and p.get_name() == profile_name
            ),
            None
        )
        if profile:
            logging.info("vNIC Profile: '%s' already defined in network: '%s'", profile_name, net)
            continue

        logging.info("Adding vNIC Profile: '%s' to network: '%s'", profile_name, net)
        vnic_profile = params.VnicProfile(name=profile_name, network=network)
        cp = params.CustomProperties([params.CustomProperty(name='vmfex', value=profile_name)])
        vnic_profile.set_custom_properties(cp)
        api.vnicprofiles.add(vnic_profile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="username")
    parser.add_argument("-url", "--url", help="API URL")
    parser.add_argument("-dc", "--datacenter", help="Data center name")
    parser.add_argument("-net", "--network", help="Network")
    parser.add_argument("-p", "--profiles", help="vNIC name")
    if len(sys.argv) != 11:
        parser.print_help()
        exit()

    args = parser.parse_args()
    password = getpass.getpass(prompt='Please enter RHV Manager admin password: ')

    api = API(url=args.url, username=args.username, password=password, insecure=True)
    try:
        create_vnic(api, args.datacenter, args.profiles, args.network)
    finally:
        api.disconnect()
