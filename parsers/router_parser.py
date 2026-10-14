def get_router_vlans(interfaces):

    vlans = []

    for interface, lines in interfaces.items():

        for line in lines:

            if "encapsulation dot1Q" in line:

                vlan = line.split()[-1]

                vlans.append(vlan)

    return vlans