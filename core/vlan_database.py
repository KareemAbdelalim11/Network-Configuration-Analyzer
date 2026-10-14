def build_vlan_database(switches):

    vlan_db = {}

    for switch in switches:

        hostname = switch["hostname"]

        for interface, vlan in switch[
            "access_vlans"
        ].items():

            if vlan not in vlan_db:

                vlan_db[vlan] = []

            vlan_db[vlan].append({

                "switch": hostname,

                "interface": interface
            })

    return vlan_db