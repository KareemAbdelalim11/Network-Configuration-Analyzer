def get_trunks(interfaces):

    trunks = {}

    for interface, lines in interfaces.items():

        trunks[interface] = {

            "mode": "access",

            "allowed_vlans": "all",

            "native_vlan": "1",

            "lines": lines
        }

        for line in lines:

            # Trunk mode

            if "switchport mode trunk" in line:

                trunks[interface]["mode"] = (
                    "trunk"
                )

            # Allowed VLANs

            if "switchport trunk allowed vlan" in line:

                trunks[interface][
                    "allowed_vlans"
                ] = line.split()[-1]

            # Native VLAN

            if "switchport trunk native vlan" in line:

                trunks[interface][
                    "native_vlan"
                ] = line.split()[-1]

    return trunks