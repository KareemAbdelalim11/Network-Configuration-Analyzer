def simulate_stp(topology):

    events = []

    devices = topology["devices"]

    links = topology["links"]

    switches = []

    # =====================================
    # DISCOVER SWITCHES
    # =====================================

    for device, data in devices.items():

        if data["type"] == "switch":

            switches.append(device)

    # =====================================
    # ROOT BRIDGE ELECTION
    # =====================================

    core_switches = [

        s for s in switches

        if "CORE" in s.upper()
    ]

    if core_switches:

        root_bridge = core_switches[0]

    else:

        root_bridge = sorted(
            switches
        )[0]

    events.append(

        f"STP Root Bridge elected: "
        f"{root_bridge}"
    )

    # =====================================
    # FIND TRUNK LINKS
    # =====================================

    trunk_links = [

        link for link in links

        if link["type"] == "trunk"
    ]

    # =====================================
    # FAILOVER SIMULATION
    # =====================================

    if len(trunk_links) > 0:

        primary_link = trunk_links[0]

        events.append(

            f"Primary trunk link failed: "

            f"{primary_link['device1']} "

            f"<-> "

            f"{primary_link['device2']}"
        )

        events.append(
            "STP recalculated topology"
        )

        # =================================
        # BACKUP LINK
        # =================================

        if len(trunk_links) > 1:

            backup_link = trunk_links[1]

            events.append(

                f"Backup path activated: "

                f"{backup_link['device1']} "

                f"<-> "

                f"{backup_link['device2']}"
            )

            events.append(
                "Backup path moved "
                "to FORWARDING state"
            )

        else:

            events.append(
                "No redundant trunk links "
                "available"
            )

    else:

        events.append(
            "No trunk links detected "
            "for STP simulation"
        )

    # =====================================
    # STP HEALTH SUMMARY
    # =====================================

    if len(trunk_links) >= 2:

        events.append(
            "Network redundancy level: GOOD"
        )

    elif len(trunk_links) == 1:

        events.append(
            "Network redundancy level: LIMITED"
        )

    else:

        events.append(
            "Network redundancy level: NONE"
        )

    return events