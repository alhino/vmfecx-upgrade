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
import sys

from ovirtsdk.api import API

"""
This script lists all UCS-M profiles used by the VMs in a given cluster.
Following is an example how to execute the script:

    python list-ucs-profiles.py -u admin@internal -url http://host/ovirt-engine/api -c clstr

"""

def get_vmfex(vm):
    if vm.get_custom_properties():
        for custom_property in vm.get_custom_properties().get_custom_property():
            if custom_property.get_name() == "vmfex":
                return custom_property.get_value()
    return None

def list_ucs_profiles(api, cluster):
    vms = api.vms.list(query='cluster=' + cluster)
    profiles = set()
    for vm in vms:
        vmfex = get_vmfex(vm)
        if not vmfex:
            continue

        vmfex_dict = ast.literal_eval(vmfex)
        for mac, profile_name in vmfex_dict.items():
            profiles.add(profile_name)

    print ','.join(profiles)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="username")
    parser.add_argument("-url", "--url", help="API URL")
    parser.add_argument("-c", "--cluster", help="Cluster")
    if len(sys.argv) != 7:
        parser.print_help()
        exit()

    args = parser.parse_args()
    password = getpass.getpass(prompt='Please enter RHV Manager admin password: ')

    api = API(url=args.url, username=args.username, password=password, insecure=True)
    try:
        list_ucs_profiles(api, args.cluster)
    finally:
        api.disconnect()
