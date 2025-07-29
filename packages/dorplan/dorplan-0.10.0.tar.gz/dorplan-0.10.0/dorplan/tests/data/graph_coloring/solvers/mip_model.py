import pulp as pl  # type: ignore[import-untyped]
from cornflow_client.constants import (  # type: ignore[import-untyped]
    STATUS_OPTIMAL,
    STATUS_INFEASIBLE,
    STATUS_UNDEFINED,
    STATUS_NOT_SOLVED,
    STATUS_UNBOUNDED,
    SOLUTION_STATUS_FEASIBLE,
    SOLUTION_STATUS_INFEASIBLE,
)
import pytups as pt  # type: ignore[import-untyped]
from ..core import Solution, Experiment


class PulpMip(Experiment):
    def solve(self, options: dict):
        model = pl.LpProblem()
        nodes = self.instance.get_nodes()
        pairs = self.instance.get_pairs()
        max_colors = len(nodes) - 1
        all_colors = range(max_colors)

        # binary if node n has color c
        node_color = pt.SuperDict(
            {
                (node, color): pl.LpVariable(
                    f"node_color_{node}_{color}", 0, 1, pl.LpBinary
                )
                for node in nodes
                for color in range(max_colors)
            }
        )
        # TODO: identify maximum cliques and apply constraint on the cliques instead of on pairs
        # colors should be different if part of pair
        for n1, n2 in pairs:
            for color in all_colors:
                model += node_color[n1, color] + node_color[n2, color] <= 1

        # max one color per node
        for node in nodes:
            model += pl.lpSum(node_color[node, color] for color in all_colors) == 1
        # objective function
        model += pl.lpSum(
            node_color[node, color] * color for node in nodes for color in all_colors
        )
        if (my_callback_obj := options.get("stop_condition", None)) and isinstance(
            my_callback_obj, StopOnUserInput
        ):
            my_callback_type = pl.HiGHS.hscb.HighsCallbackType.kCallbackMipInterrupt

            # if a callback is provided, we use it to stop the solver
            def user_callback(
                callback_type,
                message,
                data_out,
                data_in,
                user_callback_data: StopOnUserInput,
            ):
                if callback_type == my_callback_type:
                    if user_callback_data.is_stopped():
                        data_in.user_interrupt = True

            solver = pl.HiGHS(
                msg=True,
                timeLimit=options.get("timeLimit", 10),
                callbackTuple=(user_callback, my_callback_obj),
                callbacksToActivate=[my_callback_type],
            )
        else:
            solver = pl.HiGHS(msg=True, timeLimit=options.get("timeLimit", 10))

        termination_condition = model.solve(solver)
        PULP_STATUS_MAPPING = {
            pl.LpStatusOptimal: STATUS_OPTIMAL,
            pl.LpStatusInfeasible: STATUS_INFEASIBLE,
            pl.LpStatusUnbounded: STATUS_UNBOUNDED,
            pl.LpStatusNotSolved: STATUS_NOT_SOLVED,
            pl.LpStatusUndefined: STATUS_UNDEFINED,
        }
        if termination_condition not in [pl.LpStatusOptimal]:
            return dict(
                status=PULP_STATUS_MAPPING.get(termination_condition),
                status_sol=SOLUTION_STATUS_INFEASIBLE,
            )
        # get the solution
        assign_list = (
            node_color.vfilter(lambda v: pl.value(v) > 0.5)
            .keys_tl()
            .vapply(lambda v: dict(node=v[0], color=v[1]))
        )
        self.solution = Solution(dict(assignment=assign_list))

        return dict(
            status=PULP_STATUS_MAPPING.get(termination_condition),
            status_sol=SOLUTION_STATUS_FEASIBLE,
        )

    @staticmethod
    def getStopOnUser_callback():
        return StopOnUserInput()


class StopOnUserInput(object):
    def __init__(self):
        self.__stop = False

    def stop(self):
        self.__stop = True

    def is_stopped(self):
        return self.__stop
