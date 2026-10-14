def parse_config(file_path):

    try:

        with open(

            file_path,

            "r",

            encoding="utf-8",

            errors="ignore"

        ) as f:

            lines = f.readlines()

    except Exception:

        return {

            "hostname": "INVALID",

            "interfaces": {}
        }

    hostname = "UNKNOWN"

    interfaces = {}

    current_interface = None

    for line in lines:

        line = line.strip()

        # Hostname

        if line.startswith("hostname"):

            parts = line.split()

            if len(parts) > 1:

                hostname = parts[1]

        # Interface

        elif line.startswith("interface"):

            parts = line.split()

            if len(parts) > 1:

                current_interface = parts[1]

                interfaces[current_interface] = []

        elif current_interface:

            interfaces[current_interface].append(
                line
            )

    return {

        "hostname": hostname,

        "interfaces": interfaces
    }