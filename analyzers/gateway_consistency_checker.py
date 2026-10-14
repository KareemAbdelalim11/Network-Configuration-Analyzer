def check_gateway_consistency(
    gateway_ips
):

    issues = []

    vlan_gateway_map = {}

    for gateway in gateway_ips:

        vlan = gateway["vlan"]

        ip = gateway["ip"]

        if vlan not in vlan_gateway_map:

            vlan_gateway_map[vlan] = ip

        else:

            existing_ip = vlan_gateway_map[
                vlan
            ]

            if existing_ip != ip:

                issues.append(

                    f"[CRITICAL] VLAN "

                    f"{vlan} has inconsistent "

                    f"gateway assignments"
                )

    return issues