from ..core import Solution, Experiment
import networkx as nx
from cornflow_client.constants import (
    SOLUTION_STATUS_INFEASIBLE,
    SOLUTION_STATUS_FEASIBLE,
    STATUS_FEASIBLE,
    STATUS_UNDEFINED,
)


class NetworkXHeuristic(Experiment):
    def solve(self, options: dict):
        # Create the graph
        graph = self.instance.get_graph()

        # Use NetworkX's greedy coloring
        try:
            print("Starting NetworkX greedy coloring solver")
            coloring = nx.greedy_color(graph, strategy="saturation_largest_first")
            coloring = [dict(node=k, color=v) for k, v in coloring.items()]
            self.solution = Solution(dict(assignment=coloring))
            print("Finished NetworkX greedy coloring solver")

            return dict(
                status=STATUS_FEASIBLE,
                status_sol=SOLUTION_STATUS_FEASIBLE,
            )
        except Exception as e:
            return dict(
                status=STATUS_UNDEFINED,
                status_sol=SOLUTION_STATUS_INFEASIBLE,
            )
