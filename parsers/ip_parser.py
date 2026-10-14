def extract_gateway_ips(

    interfaces
):

    gateways = []

    # =====================================
    # PARSE INTERFACES
    # =====================================

    for interface, lines in interfaces.items():

        vlan = None

        ip = None

        # ---------------------------------
        # EXTRACT VLAN FROM SUBINTERFACE
        # Example:
        # GigabitEthernet0/0.10
        # ---------------------------------

        if "." in interface:

            try:

                vlan = interface.split(".")[1]

            except Exception:

                vlan = "UNKNOWN"

        # ---------------------------------
        # FIND IP ADDRESS
        # ---------------------------------

        for line in lines:

            if line.startswith(
                "ip address"
            ):

                parts = line.split()

                if len(parts) >= 3:

                    ip = parts[2]

        # ---------------------------------
        # SAVE RESULT
        # ---------------------------------

        if ip:

            gateways.append({

                "interface": interface,

                "vlan": vlan,

                "ip": ip
            })

    return gateways