def check_missing_gateways(

    switch_vlans,

    router_vlans
):

    issues = []

    for vlan in switch_vlans.values():

        if vlan not in router_vlans:

            issues.append(

                f"[CRITICAL] VLAN {vlan} "

                f"has no gateway configured"
            )

    return issues