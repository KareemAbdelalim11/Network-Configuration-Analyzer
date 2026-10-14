def get_access_vlans(interfaces):

    vlans = {}

    for interface, lines in interfaces.items():

        for line in lines:

            if "switchport access vlan" in line:

                vlan = line.split()[-1]

                vlans[interface] = vlan

    return vlans