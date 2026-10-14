from datetime import datetime


def export_html_report(report):

    timestamp = datetime.now()

    # =====================================
    # ISSUE HTML
    # =====================================

    issues_html = ""

    for issue in report["issues"]:

        # Critical

        if "[CRITICAL]" in issue:

            issues_html += f"""

            <div class="critical">
                {issue}
            </div>

            """

        # Warning

        elif "[WARNING]" in issue:

            issues_html += f"""

            <div class="warning">
                {issue}
            </div>

            """

        # Info

        else:

            issues_html += f"""

            <div class="info">
                {issue}
            </div>

            """

    # =====================================
    # ROLLBACK HTML
    # =====================================

    rollback_html = ""

    for step in report["rollback"]:

        rollback_html += f"""

        <div class="rollback">
            {step}
        </div>

        """

    # =====================================
    # SUMMARY COUNTS
    # =====================================

    critical_count = len([

        i for i in report["issues"]

        if "[CRITICAL]" in i
    ])

    warning_count = len([

        i for i in report["issues"]

        if "[WARNING]" in i
    ])

    # =====================================
    # FINAL HTML
    # =====================================

    html = f"""

    <html>

    <head>

        <title>
            VLAN Risk Analysis Report
        </title>

        <style>

            body {{

                background-color: #0f172a;

                color: white;

                font-family: Arial, sans-serif;

                margin: 40px;
            }}

            h1 {{

                color: #38bdf8;

                font-size: 42px;
            }}

            h2 {{

                color: #f8fafc;

                margin-top: 40px;
            }}

            .section {{

                background-color: #111827;

                padding: 20px;

                border-radius: 12px;

                margin-bottom: 25px;
            }}

            .summary-container {{

                display: flex;

                gap: 20px;

                margin-top: 20px;
            }}

            .summary-box {{

                flex: 1;

                padding: 20px;

                border-radius: 10px;

                text-align: center;

                font-size: 24px;

                font-weight: bold;
            }}

            .risk-score {{

                background-color: #1e293b;

                color: #38bdf8;
            }}

            .critical-box {{

                background-color: #7f1d1d;

                color: #fecaca;
            }}

            .warning-box {{

                background-color: #78350f;

                color: #fde68a;
            }}

            .critical {{

                background-color: #450a0a;

                border-left: 6px solid red;

                padding: 15px;

                margin-bottom: 10px;

                border-radius: 8px;
            }}

            .warning {{

                background-color: #422006;

                border-left: 6px solid orange;

                padding: 15px;

                margin-bottom: 10px;

                border-radius: 8px;
            }}

            .info {{

                background-color: #082f49;

                border-left: 6px solid #38bdf8;

                padding: 15px;

                margin-bottom: 10px;

                border-radius: 8px;
            }}

            .rollback {{

                background-color: #111827;

                border-left: 6px solid #22c55e;

                padding: 15px;

                margin-bottom: 10px;

                border-radius: 8px;

                font-family: monospace;
            }}

            img {{

                width: 100%;

                border-radius: 12px;

                margin-top: 20px;

                border: 2px solid #334155;
            }}

            .footer {{

                margin-top: 50px;

                text-align: center;

                color: gray;
            }}

        </style>

    </head>

    <body>

        <h1>
            VLAN Risk Analysis Report
        </h1>

        <div class="section">

            <h2>
                Analysis Information
            </h2>

            <p>
                <strong>Timestamp:</strong>
                {timestamp}
            </p>

        </div>

        <div class="summary-container">

            <div class="summary-box risk-score">

                Risk Score<br>
                {report['risk_score']}/100

            </div>

            <div class="summary-box critical-box">

                Critical Issues<br>
                {critical_count}

            </div>

            <div class="summary-box warning-box">

                Warnings<br>
                {warning_count}

            </div>

        </div>

        <div class="section">

            <h2>
                Detected Network Risks
            </h2>

            {issues_html}

        </div>

        <div class="section">

            <h2>
                Recovery Recommendations
            </h2>

            {rollback_html}

        </div>

        <div class="footer">

            Generated by VLAN Risk Platform

        </div>

    </body>

    </html>

    """

    # =====================================
    # SAVE REPORT
    # =====================================

    with open(

        "reports/report.html",

        "w",

        encoding="utf-8"

    ) as f:

        f.write(html)