import networkx as nx
import matplotlib.pyplot as plt

from topology.yaml_loader import (
    load_topology
)


def generate_topology_graph():

    topology = load_topology()

    G = nx.Graph()

    # =====================================
    # ADD DEVICES
    # =====================================

    node_colors = []

    for device, data in topology["devices"].items():

        device_type = data["type"]

        G.add_node(

            device,

            device_type=device_type
        )

    # =====================================
    # ADD LINKS
    # =====================================

    for link in topology["links"]:

        G.add_edge(

            link["device1"],

            link["device2"],

            label=link["type"]
        )

    # =====================================
    # NODE COLORS
    # =====================================

    for node in G.nodes():

        device_type = G.nodes[node][
            "device_type"
        ]

        if device_type == "switch":

            node_colors.append(
                "skyblue"
            )

        elif device_type == "router":

            node_colors.append(
                "orange"
            )

        else:

            node_colors.append(
                "lightgray"
            )

    # =====================================
    # GRAPH LAYOUT
    # =====================================

    plt.figure(

        figsize=(14, 10)
    )

    pos = nx.spring_layout(

        G,

        k=1.8,

        iterations=200,

        seed=42
    )

    # =====================================
    # DRAW NODES
    # =====================================

    nx.draw_networkx_nodes(

        G,

        pos,

        node_color=node_colors,

        node_size=4500
    )

    # =====================================
    # DRAW EDGES
    # =====================================

    nx.draw_networkx_edges(

        G,

        pos,

        width=2
    )

    # =====================================
    # DRAW LABELS
    # =====================================

    nx.draw_networkx_labels(

        G,

        pos,

        font_size=11,

        font_weight="bold"
    )

    # =====================================
    # EDGE LABELS
    # =====================================

    edge_labels = nx.get_edge_attributes(

        G,

        "label"
    )

    nx.draw_networkx_edge_labels(

        G,

        pos,

        edge_labels=edge_labels,

        font_size=9
    )

    # =====================================
    # TITLE
    # =====================================

    plt.title(

        "Topology-Aware Network Graph",

        fontsize=18,

        fontweight="bold"
    )

    plt.axis("off")

    plt.tight_layout()

    # =====================================
    # SAVE GRAPH
    # =====================================

    plt.savefig(

        "reports/topology.png",

        dpi=300,

        bbox_inches="tight"
    )

    plt.close()