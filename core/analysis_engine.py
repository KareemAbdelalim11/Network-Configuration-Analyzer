from parsers.vlan_parser import (
    get_access_vlans
)

from parsers.trunk_parser import (
    get_trunks
)

from parsers.router_parser import (
    get_router_vlans
)

from parsers.ip_parser import (
    extract_gateway_ips
)

from analyzers.vlan_checker import (
    check_missing_gateways
)

from analyzers.trunk_checker import (
    check_trunk_vlans
)

from analyzers.native_vlan_checker import (
    check_native_vlan_mismatch
)

from analyzers.svi_checker import (
    check_missing_svis
)

from analyzers.risk_score import (
    calculate_risk_score
)

from analyzers.rollback_generator import (
    generate_rollback
)

from analyzers.duplicate_gateway_checker import (
    check_duplicate_gateways
)

from analyzers.gateway_consistency_checker import (
    check_gateway_consistency
)


def analyze_network(devices):

    issues = []

    switches = []

    routers = []

    router_vlans = []

    gateway_ips = []

    device_summary = []


    # =====================================
    # PARSE DEVICES
    # =====================================

    for device in devices:

        hostname = device["hostname"]

        device_type = device["type"]

        interfaces = device["interfaces"]

        # ---------------------------------
        # SWITCH PROCESSING
        # ---------------------------------

        if device_type == "switch":

            access_vlans = get_access_vlans(
                interfaces
            )

            trunks = get_trunks(
                interfaces
            )

            device["access_vlans"] = (
                access_vlans
            )

            device["trunks"] = trunks

            switches.append(device)

            device_summary.append({

                "hostname": hostname,

                "type": "switch",

                "vlans": list(
                    access_vlans.values()
                ),

                "trunk_count": len([
                    t for t in trunks.values()
                    if t["mode"] == "trunk"
                ])
            })

        # ---------------------------------
        # ROUTER PROCESSING
        # ---------------------------------

        elif device_type == "router":

            vlans = get_router_vlans(
                interfaces
            )

            router_vlans.extend(vlans)

            ips = extract_gateway_ips(
                interfaces
            )

            gateway_ips.extend(ips)

            routers.append(device)

            device_summary.append({

                "hostname": hostname,

                "type": "router",

                "gateway_count": len(ips),

                "vlans": vlans
            })


    # =====================================
    # SWITCH ANALYSIS
    # =====================================

    for switch in switches:

        # ---------------------------------
        # MISSING GATEWAYS
        # ---------------------------------

        issues.extend(

            check_missing_gateways(

                switch["access_vlans"],

                router_vlans
            )
        )

        # ---------------------------------
        # MISSING SVIs
        # ---------------------------------

        issues.extend(

            check_missing_svis(

                switches,
                router_vlans
            )
        )

        # ---------------------------------
        # TRUNK VALIDATION
        # ---------------------------------

        issues.extend(

            check_trunk_vlans(

                switches
            )
        )


    # =====================================
    # NATIVE VLAN MISMATCH
    # =====================================

    issues.extend(

        check_native_vlan_mismatch(
            switches
        )
    )


    # =====================================
    # DUPLICATE GATEWAY IP CHECK
    # =====================================

    issues.extend(

        check_duplicate_gateways(
            gateway_ips
        )
    )

    # =====================================
    # INCONSISTENT GATEWAY ASSIGNMENTS
    # =====================================

    issues.extend(

        check_gateway_consistency(
            gateway_ips
        )
    )


    # =====================================
    # REMOVE DUPLICATES
    # =====================================

    issues = list(set(issues))


    # =====================================
    # RISK SCORE
    # =====================================

    risk_score = calculate_risk_score(
        issues
    )


    # =====================================
    # ROLLBACK RECOMMENDATIONS
    # =====================================

    rollback = generate_rollback(
        issues
    )


    # =====================================
    # IMPACT SUMMARY
    # =====================================

    impacted_vlans = []

    for issue in issues:

        if "VLAN" in issue:

            parts = issue.split()

            for part in parts:

                if part.isdigit():

                    impacted_vlans.append(
                        part
                    )

    impacted_vlans = list(
        set(impacted_vlans)
    )


    # =====================================
    # RETURN REPORT
    # =====================================

    return {

        "issues": issues,

        "risk_score": risk_score,

        "rollback": rollback,

        "switches": switches,

        "routers": routers,

        "router_vlans": router_vlans,

        "gateway_ips": gateway_ips,

        "impacted_vlans": impacted_vlans,

        "device_summary": device_summary
    }