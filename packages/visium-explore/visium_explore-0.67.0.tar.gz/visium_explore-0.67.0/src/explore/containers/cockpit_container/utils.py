"""Function to read dvc.yaml and parse the DVC graph into nodes and edges."""


def parse_dvc_graph(dvc_yaml: dict) -> tuple[list[str], list[tuple[str, str]]]:
    """Parse the DVC graph from the dictionary representation of dvc.yaml."""
    stages_dict = dvc_yaml["stages"]
    nodes = []
    for stage in stages_dict:
        nodes.append(stage)

    edges = []
    for stage_name, stage_content in stages_dict.items():
        outs = stage_content["outs"]
        assert len(outs) == 1, "There should be only one output per step"
        out = outs[0]
        for inner_stage_name, inner_stage_content in stages_dict.items():
            deps = inner_stage_content["deps"]
            for dep in deps:
                if dep == out:
                    edges.append((stage_name, inner_stage_name))
    return nodes, edges
