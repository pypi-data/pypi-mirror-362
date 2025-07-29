from ortools.sat.python import cp_model
from cornflow_client.constants import (  # type: ignore[import-untyped]
    STATUS_FEASIBLE,
    STATUS_INFEASIBLE,
    STATUS_OPTIMAL,
    STATUS_UNDEFINED,
    SOLUTION_STATUS_FEASIBLE,
    SOLUTION_STATUS_INFEASIBLE,
)
import pytups as pt  # type: ignore[import-untyped]
from ..core import Solution, Experiment


class OrToolsCP(Experiment):
    def solve(self, options: dict):
        model = cp_model.CpModel()
        input_data = pt.SuperDict.from_dict(self.instance.data)
        nodes = self.instance.get_nodes()
        pairs = input_data["pairs"]
        max_colors = len(nodes) - 1

        # variable declaration:
        color = pt.SuperDict(
            {
                node: model.NewIntVar(0, max_colors, "color_{}".format(node))
                for node in nodes
            }
        )
        # TODO: identify maximum cliques and apply constraint on the cliques instead of on pairs
        for pair in pairs:
            model.Add(color[pair["n1"]] != color[pair["n2"]])

        obj_var = model.NewIntVar(0, max_colors, "total_colors")
        model.AddMaxEquality(obj_var, color.values())
        model.Minimize(obj_var)
        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        # solver.log_callback = print
        solver.parameters.log_to_stdout = True
        solver.parameters.max_time_in_seconds = options.get("timeLimit", 10)
        termination_condition = solver.Solve(model)
        ortools_status_map = {
            cp_model.OPTIMAL: STATUS_OPTIMAL,
            cp_model.FEASIBLE: STATUS_FEASIBLE,
            cp_model.INFEASIBLE: STATUS_INFEASIBLE,
        }
        if termination_condition not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return dict(
                status=ortools_status_map.get(termination_condition, STATUS_UNDEFINED),  # type: ignore[call-overload]
                status_sol=SOLUTION_STATUS_INFEASIBLE,
            )
        color_sol = color.vapply(solver.Value)

        assign_list = color_sol.items_tl().vapply(lambda v: dict(node=v[0], color=v[1]))
        self.solution = Solution(dict(assignment=assign_list))

        return dict(
            status=ortools_status_map.get(termination_condition, STATUS_UNDEFINED),  # type: ignore[call-overload]
            status_sol=SOLUTION_STATUS_FEASIBLE,
        )
