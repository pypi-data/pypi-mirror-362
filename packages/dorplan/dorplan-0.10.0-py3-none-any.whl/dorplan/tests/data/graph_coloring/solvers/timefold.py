from typing import Any
from typing import Annotated
from pydantic import Field
from dataclasses import dataclass, field
from pytups import TupList, SuperDict
from pydantic import PlainSerializer, BeforeValidator
import os
import logging.config

from ..core import Experiment, Solution
from cornflow_client.constants import SOLUTION_STATUS_FEASIBLE

from timefold.solver.domain import (
    ValueRangeProvider,
    PlanningVariable,
    PlanningId,
    planning_entity,
    planning_solution,
    PlanningEntityCollectionProperty,
    ProblemFactCollectionProperty,
    PlanningScore,
)
from timefold.solver.score import (
    constraint_provider,
    ConstraintFactory,
    Joiners,
    Constraint,
    HardSoftScore,
    HardSoftDecimalScore,
)
from timefold.solver import SolverFactory, SolutionManager
from timefold.solver.config import (
    SolverConfig,
    ScoreDirectorFactoryConfig,
    TerminationConfig,
    Duration,
)


@dataclass
@planning_entity
class Node:
    id: Annotated[int, PlanningId]
    color: Annotated[
        int | None,
        PlanningVariable(value_range_provider_refs=["colorRange"]),
        Field(default=None),
    ]


@dataclass
class Arc:
    id: int
    node1: int
    node2: int


ScoreSerializer = PlainSerializer(
    lambda score: str(score) if score is not None else None, return_type=str | None
)


def validate_score(v: Any) -> Any:
    if isinstance(v, HardSoftDecimalScore) or v is None:
        return v
    if isinstance(v, str):
        return HardSoftDecimalScore.parse(v)
    raise ValueError('"score" should be a string')


ScoreValidator = BeforeValidator(validate_score)


@dataclass
@planning_solution
class GraphColoringSolution:
    nodes: Annotated[list[Node], PlanningEntityCollectionProperty, ValueRangeProvider]
    arcs: Annotated[list[Arc], ProblemFactCollectionProperty, ValueRangeProvider]
    colorRange: Annotated[list[int], ValueRangeProvider(id="colorRange")] = field(
        default_factory=list
    )
    # weight_overrides: ConstraintWeightOverrides
    score: Annotated[
        HardSoftScore | None, PlanningScore, ScoreSerializer, ScoreValidator
    ] = field(default=None)


@constraint_provider
def define_constraints(factory: ConstraintFactory):
    return [different_color(factory), min_colors(factory), assign_color(factory)]


def different_color(factory: ConstraintFactory) -> Constraint:
    return (
        factory.for_each(Arc)
        .join(Node, Joiners.equal(lambda arc: arc.node1, lambda node: node.id))
        .join(Node, Joiners.equal(lambda arc, n1: arc.node2, lambda node: node.id))
        .filter(lambda arc, n1, n2: n1.color == n2.color)
        # .filter(lambda arc: arc.node1.color is not None and arc.node2.color is not None)
        # .filter(lambda arc: arc.node1.color == arc.node2.color)
        .penalize(HardSoftScore.ONE_HARD)
        .as_constraint("Different color for connected nodes")
    )


def assign_color(factory: ConstraintFactory) -> Constraint:
    return (
        factory.for_each_including_unassigned(Node)
        .filter(lambda node: node.color is None)
        .penalize(HardSoftScore.ONE_HARD, lambda node: 1)
        .as_constraint("Assign color to uncolored nodes")
    )


def min_colors(factory: ConstraintFactory) -> Constraint:
    return (
        factory.for_each(Node)
        .penalize(HardSoftScore.ONE_SOFT, lambda node: node.color)
        .as_constraint("Minimize the number of colors used")
    )


class TimefoldPy(Experiment):
    def solve(self, options: dict = None) -> dict:
        """
        Solve the graph coloring problem using Timefold solver.
        :param options:
        :return:
        """
        if options is None:
            options = {}
        my_dir = os.path.dirname(__file__)
        logging.config.fileConfig(os.path.join(my_dir, "logging.conf"))
        solver_factory = SolverFactory.create(
            SolverConfig(
                solution_class=GraphColoringSolution,
                entity_class_list=[Node],
                score_director_factory_config=ScoreDirectorFactoryConfig(
                    constraint_provider_function=define_constraints
                ),
                termination_config=TerminationConfig(
                    spent_limit=Duration(seconds=options.get("timeLimit", 30))
                ),
            )
        )
        my_nodes = {
            node_id: Node(id=node_id, color=None)
            for node_id in self.instance.get_nodes()
        }
        # solver.terminate_early()
        my_arcs = [
            Arc(id=arc_id, node1=arc[0], node2=arc[1])
            for arc_id, arc in enumerate(self.instance.get_pairs())
        ]
        color_range = list(range(len(my_nodes)))
        problem = GraphColoringSolution(
            nodes=list(my_nodes.values()), arcs=my_arcs, colorRange=color_range
        )
        solver = solver_factory.build_solver()

        if my_obj := options.get("stop_condition", None):
            if isinstance(my_obj, StopOnUserInput):
                my_obj.set_solver(solver)

        solution = solver.solve(problem)
        solution_manager = SolutionManager.create(solver_factory)
        analysis = solution_manager.analyze(solution)
        print(analysis.summary)
        sol_data = TupList(
            SuperDict(node=node.id, color=node.color) for node in solution.nodes
        )
        self.solution = Solution.from_dict(dict(assignment=sol_data))
        # get solution, status
        return dict(status=1, status_sol=SOLUTION_STATUS_FEASIBLE)

    @staticmethod
    def getStopOnUser_callback():
        return StopOnUserInput()


class StopOnUserInput(object):
    def __init__(self):
        self.__stop = False
        self.__solver = None

    def set_solver(self, solver):
        self.__solver = solver

    def stop(self):
        if self.__solver is not None:
            self.__solver.terminate_early()
        else:
            logging.warning("Solver not set, cannot stop.")
        self.__stop = True

    def is_stopped(self):
        return self.__stop
