import os

from parsers.config_parser import (
    parse_config
)


def discover_devices():

    devices = []

    upload_folder = "uploads"

    for file in os.listdir(upload_folder):

        if file.endswith(".txt"):

            path = os.path.join(

                upload_folder,

                file
            )

            parsed = parse_config(path)

            hostname = parsed["hostname"]

            interfaces = parsed["interfaces"]

            # Detect router or switch

            is_router = False

            for intf in interfaces:

                if "." in intf:

                    is_router = True

            device_type = (
                "router"
                if is_router
                else "switch"
            )

            devices.append({

                "hostname": hostname,

                "type": device_type,

                "interfaces": interfaces,

                "file": file
            })

    return devices