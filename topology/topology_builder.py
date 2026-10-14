import yaml

from parsers.trunk_parser import (
    get_trunks
)


def build_topology(devices):

    topology = {

        "devices": {},

        "links": []
    }

    switches = []

    routers = []

    # =====================================
    # INVENTORY
    # =====================================

    for device in devices:

        hostname = device["hostname"]

        topology["devices"][hostname] = {

            "type": device["type"]
        }

        # -------------------------------

        if device["type"] == "switch":

            switches.append(device)

        elif device["type"] == "router":

            routers.append(device)

    # =====================================
    # SORT SWITCHES BY ROLE
    # =====================================

    core_switches = []

    dist_switches = []

    access_switches = []

    other_switches = []

    for switch in switches:

        hostname = switch[
            "hostname"
        ].upper()

        if "CORE" in hostname:

            core_switches.append(switch)

        elif "DIST" in hostname:

            dist_switches.append(switch)

        elif "ACCESS" in hostname:

            access_switches.append(switch)

        else:

            other_switches.append(switch)

    # =====================================
    # CORE -> DIST LINKS
    # =====================================

    for core in core_switches:

        for dist in dist_switches:

            topology["links"].append({

                "device1": core[
                    "hostname"
                ],

                "interface1": "trunk",

                "device2": dist[
                    "hostname"
                ],

                "interface2": "trunk",

                "type": "trunk"
            })

    # =====================================
    # DIST -> ACCESS LINKS
    # =====================================

    for dist in dist_switches:

        for access in access_switches:

            topology["links"].append({

                "device1": dist[
                    "hostname"
                ],

                "interface1": "trunk",

                "device2": access[
                    "hostname"
                ],

                "interface2": "trunk",

                "type": "trunk"
            })

    # =====================================
    # OTHER SWITCH LINKS
    # =====================================

    for i in range(

        len(other_switches) - 1
    ):

        topology["links"].append({

            "device1": other_switches[i][
                "hostname"
            ],

            "interface1": "trunk",

            "device2": other_switches[i + 1][
                "hostname"
            ],

            "interface2": "trunk",

            "type": "trunk"
        })

    # =====================================
    # ROUTER UPLINKS
    # =====================================

    uplink_target = None

    # Prefer CORE

    if core_switches:

        uplink_target = core_switches[0]

    elif dist_switches:

        uplink_target = dist_switches[0]

    elif access_switches:

        uplink_target = access_switches[0]

    elif switches:

        uplink_target = switches[0]

    # Create router uplinks

    if uplink_target:

        for router in routers:

            topology["links"].append({

                "device1": uplink_target[
                    "hostname"
                ],

                "interface1": "uplink",

                "device2": router[
                    "hostname"
                ],

                "interface2": "Gig0/0",

                "type": "uplink"
            })

    # =====================================
    # REMOVE DUPLICATE LINKS
    # =====================================

    unique_links = []

    seen = set()

    for link in topology["links"]:

        pair = tuple(

            sorted([

                link["device1"],

                link["device2"]
            ])
        )

        if pair not in seen:

            seen.add(pair)

            unique_links.append(link)

    topology["links"] = unique_links

    # =====================================
    # SAVE YAML
    # =====================================

    with open(

        "topology/topology.yaml",

        "w"

    ) as f:

        yaml.dump(

            topology,

            f,

            sort_keys=False
        )

    return topology