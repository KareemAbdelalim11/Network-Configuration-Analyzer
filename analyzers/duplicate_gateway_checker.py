def check_duplicate_gateways(

    gateway_ips
):

    issues = []

    seen = {}

    for gateway in gateway_ips:

        ip = gateway["ip"]

        interface = gateway["interface"]

        if ip in seen:

            issues.append(

                f"[CRITICAL] Duplicate "

                f"gateway IP detected: "

                f"{ip}"
            )

        else:

            seen[ip] = interface

    return issues