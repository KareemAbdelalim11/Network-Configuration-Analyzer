import yaml


def load_topology():

    with open(

        "topology/topology.yaml",

        "r"

    ) as f:

        topology = yaml.safe_load(f)

    return topology