def check_native_vlan_mismatch(

    switches
):

    issues = []

    native_vlans = {}

    for switch in switches:

        hostname = switch["hostname"]

        trunks = switch["trunks"]

        for interface, data in trunks.items():

            if data["mode"] == "trunk":

                native = data["native_vlan"]

                if interface not in native_vlans:

                    native_vlans[interface] = []

                native_vlans[interface].append(

                    (hostname, native)
                )

    for interface, values in native_vlans.items():

        detected = set()

        for hostname, vlan in values:

            detected.add(vlan)

        if len(detected) > 1:

            issues.append(

                f"[WARNING] Native VLAN "

                f"mismatch detected "

                f"on {interface}"
            )

    return issues