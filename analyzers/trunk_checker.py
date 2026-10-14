def check_trunk_vlans(

    switches
):

    issues = []

    reported = set()

    # =====================================
    # COLLECT REQUIRED VLANS
    # =====================================

    required_vlans = set()

    for switch in switches:

        access_vlans = switch[
            "access_vlans"
        ]

        for vlan in access_vlans.values():

            required_vlans.add(vlan)

    # =====================================
    # VALIDATE TRUNKS
    # =====================================

    for switch in switches:

        hostname = switch["hostname"]

        trunks = switch["trunks"]

        for interface, data in trunks.items():

            # ---------------------------------
            # ONLY TRUNK PORTS
            # ---------------------------------

            if data["mode"] != "trunk":

                continue

            allowed = data[
                "allowed_vlans"
            ]

            # ---------------------------------
            # ALL VLANS ALLOWED
            # ---------------------------------

            if allowed == "all":

                continue

            allowed_vlans = set(

                vlan.strip()

                for vlan in allowed.split(",")

                if vlan.strip()
            )

            # =================================
            # CHECK REQUIRED VLANS
            # =================================

            for vlan in required_vlans:

                if vlan not in allowed_vlans:

                    issue = (

                        f"[CRITICAL] VLAN "

                        f"{vlan} missing "

                        f"on trunk "

                        f"{interface} "

                        f"({hostname})"
                    )

                    # -------------------------
                    # PREVENT DUPLICATES
                    # -------------------------

                    unique_key = (

                        vlan,

                        hostname,

                        interface
                    )

                    if unique_key not in reported:

                        reported.add(
                            unique_key
                        )

                        issues.append(
                            issue
                        )

    # =====================================
    # SORT RESULTS
    # =====================================

    issues = sorted(issues)

    return issues