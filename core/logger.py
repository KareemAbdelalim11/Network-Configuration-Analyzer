from datetime import datetime


def log_event(message):

    timestamp = datetime.now()

    with open(

        "reports/audit.log",

        "a"

    ) as f:

        f.write(

            f"[{timestamp}] "

            f"{message}\n"
        )