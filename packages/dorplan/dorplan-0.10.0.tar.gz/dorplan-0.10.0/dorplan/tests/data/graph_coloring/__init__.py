from cornflow_client import (  # type: ignore[import-untyped]
    get_empty_schema,
    ApplicationCore,
    InstanceCore,
    SolutionCore,
    ExperimentCore,
)
from cornflow_client.core.tools import load_json  # type: ignore[import-untyped]
from typing import List, Dict
import os

Instance = InstanceCore


class GraphColoring(ApplicationCore):
    name = "graph_coloring"

    try:
        from .solvers import OrToolsCP, PulpMip, TimefoldPy, NetworkXHeuristic

        global Instance
        from .core import Instance, Solution, Experiment

        instance = Instance
        solution = Solution
        solvers = dict(
            ortools=OrToolsCP,
            pulp=PulpMip,
            timefold=TimefoldPy,
            networkx=NetworkXHeuristic,
        )
        schema = load_json(
            os.path.join(os.path.dirname(__file__), "schemas/config.json")
        )

        @property
        def test_cases(self) -> List[Dict]:

            file_dir = os.path.join(os.path.dirname(__file__), "data")
            get_file = lambda name: os.path.join(file_dir, name)
            return [
                {
                    "name": "gc_4_1",
                    "instance": Instance.from_txt_file(get_file("gc_4_1")).to_dict(),
                    "description": "Example data with 4 pairs",
                },
                {
                    "name": "gc_50_1",
                    "instance": Instance.from_txt_file(get_file("gc_50_1")).to_dict(),
                    "description": "Example data with 50 pairs",
                },
            ]

    except ImportError as e:
        print(e)
        instance = InstanceCore
        solution = SolutionCore
        solvers = dict(experiment=ExperimentCore)
        schema = get_empty_schema(solvers=["experiment"])

        @property
        def test_cases(self) -> List[Dict]:
            return [dict()]
