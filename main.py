from core.device_discovery import (
    discover_devices
)

from core.analysis_engine import (
    analyze_network
)

from topology.topology_builder import (
    build_topology
)

from topology.topology_graph import (
    generate_topology_graph
)

from core.connectivity_test import (
    run_connectivity_tests
)

from core.impact_engine import (
    predict_connectivity_impact
)

from core.stp_engine import (
    simulate_stp
)

from core.html_report import (
    export_html_report
)


# ==========================================
# DISCOVER DEVICES
# ==========================================

devices = discover_devices()

# ==========================================
# NO DEVICES FOUND
# ==========================================

if not devices:

    print(
        "\n[ERROR] "
        "No valid network devices found."
    )

    exit()

# ==========================================
# BUILD TOPOLOGY
# ==========================================

topology = build_topology(
    devices
)

# ==========================================
# GENERATE TOPOLOGY GRAPH
# ==========================================

generate_topology_graph()

# ==========================================
# ANALYZE NETWORK
# ==========================================

report = analyze_network(
    devices
)

# ==========================================
# CONNECTIVITY TESTS
# ==========================================

tests = run_connectivity_tests(

    report["issues"],

    report["switches"]
)

# ==========================================
# IMPACT PREDICTION
# ==========================================

impacts = predict_connectivity_impact(

    report["issues"]
)

# ==========================================
# STP SIMULATION
# ==========================================

stp_events = simulate_stp(
    topology
)

# ==========================================
# EXPORT HTML REPORT
# ==========================================

export_html_report(
    report
)

# ==========================================
# FINAL REPORT
# ==========================================

print(
    "\n========== VLAN RISK REPORT ==========\n"
)

# ==========================================
# RISK SCORE
# ==========================================

print(

    f"Overall Network Risk: "

    f"{report['risk_score']}/100"
)

# ==========================================
# DEVICE SUMMARY
# ==========================================

print(
    "\n========== DEVICES ==========\n"
)

for device in report[
    "device_summary"
]:

    print(

        f"{device['hostname']} "

        f"({device['type']})"
    )

# ==========================================
# DETECTED ISSUES
# ==========================================

print(
    "\n========== DETECTED ISSUES ==========\n"
)

if not report["issues"]:

    print(
        "No issues detected."
    )

else:

    for issue in report["issues"]:

        print(issue)

# ==========================================
# CONNECTIVITY IMPACT
# ==========================================

print(
    "\n========== CONNECTIVITY IMPACT ==========\n"
)

if not impacts:

    print(
        "No connectivity impact predicted."
    )

else:

    for impact in impacts:

        print(impact)

# ==========================================
# CONNECTIVITY TESTS
# ==========================================

print(
    "\n========== CONNECTIVITY TESTS ==========\n"
)

for test in tests:

    if test["status"] == "SUCCESS":

        print(

            f"{test['test']} "

            f"-> SUCCESS"
        )

    else:

        print(

            f"{test['test']} "

            f"-> FAILED "

            f"({test['reason']})"
        )

# ==========================================
# STP EVENTS
# ==========================================

print(
    "\n========== STP SIMULATION ==========\n"
)

for event in stp_events:

    print(event)

# ==========================================
# ROLLBACK STEPS
# ==========================================

print(
    "\n========== RECOVERY RECOMMENDATIONS ==========\n"
)

if not report["rollback"]:

    print(
        "No rollback actions required."
    )

else:

    for step in report["rollback"]:

        print(step)

# ==========================================
# TOPOLOGY GRAPH
# ==========================================

print(
    "\nTopology graph generated:"
)

print(
    "reports/topology.png"
)

# ==========================================
# HTML REPORT
# ==========================================

print(
    "\nHTML report generated:"
)

print(
    "reports/report.html"
)

print(
    "\n=====================================\n"
)