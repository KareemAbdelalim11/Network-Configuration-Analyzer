def check_missing_svis(

    switches,

    router_vlans
):

    issues = []

    required_vlans = set()

    # =====================================
    # COLLECT ALL ACCESS VLANS
    # =====================================

    for switch in switches:

        for vlan in switch[
            "access_vlans"
        ].values():

            required_vlans.add(vlan)

    # =====================================
    # CHECK ROUTER GATEWAYS
    # =====================================

    for vlan in required_vlans:

        if vlan not in router_vlans:

            issues.append(

                f"[CRITICAL] Missing "

                f"SVI/gateway for "

                f"VLAN {vlan}"
            )

    return issues