import os
import streamlit as st
import pandas as pd

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

from core.html_report import (
    export_html_report
)

from core.logger import (
    log_event
)

from core.stp_engine import (
    simulate_stp
)

from core.impact_engine import (
    predict_connectivity_impact
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="VLAN Risk Platform",

    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title(
    "Topology-Aware VLAN Risk Analyzer"
)

st.subheader(
    "Enterprise Network Validation Platform"
)


# ==========================================
# FILE UPLOADS
# ==========================================

st.header(
    "Upload Network Files"
)

uploaded_files = st.file_uploader(

    "Upload Cisco Configuration Files",

    type=["txt"],

    accept_multiple_files=True
)



# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button(
    "Analyze Network"
):

    if uploaded_files:

        # ==================================
        # CREATE DIRECTORIES
        # ==================================

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        os.makedirs(
            "reports",
            exist_ok=True
        )

        # ==================================
        # CLEAN OLD FILES
        # ==================================

        for file in os.listdir(
            "uploads"
        ):

            path = os.path.join(
                "uploads",
                file
            )

            if os.path.isfile(path):

                os.remove(path)

        # ==================================
        # SAVE CONFIG FILES
        # ==================================

        for file in uploaded_files:

            with open(

                f"uploads/{file.name}",

                "wb"

            ) as f:

                f.write(
                    file.getbuffer()
                )



        # ==================================
        # START LOGGING
        # ==================================

        log_event(
            "Network analysis started"
        )

        # ==================================
        # DEVICE DISCOVERY
        # ==================================

        devices = discover_devices()

        # ==================================
        # BUILD TOPOLOGY
        # ==================================

        topology = build_topology(
            devices
        )

        # ==================================
        # GENERATE GRAPH
        # ==================================

        generate_topology_graph()

        # ==================================
        # ANALYZE NETWORK
        # ==================================

        report = analyze_network(
            devices
        )

        # ==================================
        # CONNECTIVITY TESTS
        # ==================================

        tests = run_connectivity_tests(

            report["issues"]
        )

        # ==================================
        # IMPACT PREDICTION
        # ==================================

        impacts = predict_connectivity_impact(

            report["issues"]
        )

        # ==================================
        # STP SIMULATION
        # ==================================

        stp_events = simulate_stp(
            topology
        )

        # ==================================
        # EXPORT REPORT
        # ==================================

        export_html_report(
            report
        )

        # ==================================
        # LOG COMPLETE
        # ==================================

        log_event(
            "Analysis completed successfully"
        )

        # ==================================
        # RISK SCORE
        # ==================================

        st.metric(

            label="Overall Network Risk",

            value=f"{report['risk_score']}/100"
        )

        # ==================================
        # RISK VISUALIZATION
        # ==================================

        st.header(
            "Risk Summary"
        )

        chart_data = pd.DataFrame({

            "Category": [

                "Critical",

                "Warning"
            ],

            "Count": [

                len([
                    i for i in report["issues"]
                    if "[CRITICAL]" in i
                ]),

                len([
                    i for i in report["issues"]
                    if "[WARNING]" in i
                ])
            ]
        })

        st.bar_chart(

            chart_data.set_index(
                "Category"
            )
        )

        # ==================================
        # DEVICE SUMMARY
        # ==================================

        st.header(
            "Discovered Devices"
        )

        for device in report[
            "device_summary"
        ]:

            st.info(

                f"{device['hostname']} "

                f"({device['type']})"
            )

        # ==================================
        # DETECTED ISSUES
        # ==================================

        st.header(
            "Detected Network Risks"
        )

        if not report["issues"]:

            st.success(
                "No issues detected"
            )

        else:

            for issue in report["issues"]:

                if "[CRITICAL]" in issue:

                    st.error(issue)

                elif "[WARNING]" in issue:

                    st.warning(issue)

                else:

                    st.info(issue)

        # ==================================
        # IMPACT PREDICTION
        # ==================================

        st.header(
            "Predicted Connectivity Impact"
        )

        if not impacts:

            st.success(
                "No connectivity impact predicted"
            )

        else:

            for impact in impacts:

                st.warning(impact)

        # ==================================
        # CONNECTIVITY TESTS
        # ==================================

        st.header(
            "Connectivity Test Evidence"
        )

        for test in tests:

            if test["status"] == "SUCCESS":

                st.success(

                    f"{test['test']} "
                    f"-> SUCCESS"
                )

            else:

                st.error(

                    f"{test['test']} "
                    f"-> FAILED"
                    f"({test['reason']})"
                )

        # ==================================
        # STP EVENTS
        # ==================================

        st.header(
            "STP Simulation"
        )

        for event in stp_events:

            st.info(event)

        # ==================================
        # ROLLBACK
        # ==================================

        st.header(
            "Recovery Recommendations"
        )

        if not report["rollback"]:

            st.success(
                "No rollback actions required"
            )

        else:

            for step in report["rollback"]:

                st.code(step)

        # ==================================
        # TOPOLOGY GRAPH
        # ==================================

        st.header(
            "Parsed Topology Graph"
        )

        st.image(
            "reports/topology.png"
        )

        # ==================================
        # DOWNLOAD REPORT
        # ==================================

        st.header(
            "Export Analysis Report"
        )

        with open(

            "reports/report.html",

            "r"

        ) as f:

            st.download_button(

                "Download HTML Report",

                f,

                file_name="network_report.html"
            )

    else:

        st.error(
            "Please upload Cisco configuration files"
        )