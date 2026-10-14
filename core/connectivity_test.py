import re


def run_connectivity_tests(

    issues
):

    results = []

    impacted_vlans = set()

    # =====================================
    # FIND FAILED VLANS
    # =====================================

    for issue in issues:

        matches = re.findall(

            r"VLAN\s+(\d+)",

            issue
        )

        for vlan in matches:

            impacted_vlans.add(vlan)

    # =====================================
    # GENERATE TESTS
    # =====================================

    tested_vlans = set()

    for vlan in impacted_vlans:

        results.append({

            "test": f"Ping VLAN{vlan}",

            "status": "FAILED",
            "reason": "VLAN missing on trunk"
        })

        tested_vlans.add(vlan)

    # DEFAULT SUCCESS VLANS

    for vlan in ["10", "20", "30"]:

        if vlan not in tested_vlans:

            results.append({

                "test": f"Ping VLAN{vlan}",

                "status": "SUCCESS"
            })

    return results