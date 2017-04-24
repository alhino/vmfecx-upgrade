vmfex-upgrade-3.5-to-3.6.py
==========================
This script is used to update VM-FEX for VMs from 3.5 version to 3.6.
Following is an example how to run the script:

    python vmfex-upgrade-3.5-to-3.6.py -u admin@internal -url http://host/ovirt-engine/api -dc test-dc -dest-net destination-network -vms vm1,vm2,vm3 -c new_cluster

Where:
* dc: the datacenter where the VM is running
* dest-net: the destination network whetre thte vnic profile is defined
* c: destination cluster (where RHEL7 hosts are created) to move the VM to

Before running the script, please make sure that:
1. The VM is down
2. The user must create vnic profiles for each UCS-M profile used, and the name of the vnic profile must match the name of the UCSM profile

Plese note that the old vmfex custom property is removed after running the script.

create-vnic-profiles.py
======================
This script is used to add vNIC profiles to a specified network.
This script is a helper to the other script here, that can be used to for creating vNIC profiles per defined UCS profiles.
Following is an example how to run the script:

    python create-vnic-profiles.py -u admin@internal -url http://localhost:8080/ovirt-engine/api -dc dc41 -net net2 -p test,test2,test3,test4

Where:
* dc: the datacenter where the network exists
* net: the network to add vNIC profiles to
* p: comma separated list if vNIC profile names (these profiles supposed to be the UCS profiles used by VMFEX)

Notes:
1. A VMFEX custom property will be added to the vNIC profiles with the value equals to the profile name
2. If the vNIC profile exists, a message is displayed and the script will continue adding the other specified profiles

Following is a complete example of using the script
===================================================
Suppose we want to upgrade an existing VM, test-vm, that has the following VMFEX custom property:

    {'mac-addr1': 'UCS-PROFILE-1', 'mac-addr2': 'UCS-PROFILE-2'}

To upgrade that VM:
1. Run following script to create the corresponding vNIC profiles:

    python create-vnic-profiles.py -u admin@internal -url http://host/ovirt-engine/api -dc dc36 -net new-network -p UCS-PROFILE-1,UCS-PROFILE-2

2. Run the following script to upgrade the VM:

    python vmfex-upgrade-3.5-to-3.6.py -u admin@internal -url http://host/ovirt-engine/api -dc dc36 -dest-net new-network -vms test-vm -c new_cluster
