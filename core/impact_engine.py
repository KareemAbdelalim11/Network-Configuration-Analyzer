import re


def predict_connectivity_impact(

    issues
):

    impacts = []

    impacted_vlans = set()

    # =====================================
    # EXTRACT VLANS
    # =====================================

    for issue in issues:

        matches = re.findall(

            r"VLAN\s+(\d+)",

            issue
        )

        for vlan in matches:

            impacted_vlans.add(vlan)

    # =====================================
    # GENERATE IMPACTS
    # =====================================

    for vlan in impacted_vlans:

        impacts.append(

            f"Devices in VLAN {vlan} "

            f"may lose connectivity"
        )

    # =====================================
    # NATIVE VLAN
    # =====================================

    for issue in issues:

        if "Native VLAN" in issue:

            impacts.append(

                "Possible STP instability "
                "or untagged traffic leaks"
            )

    return list(set(impacts))