from cornflow_client import ExperimentCore  # type: ignore[import-untyped]
from cornflow_client.core.tools import load_json  # type: ignore[import-untyped]
from pytups import TupList  # type: ignore[import-untyped]
from .instance import Instance
from .solution import Solution
import os
import tempfile
import json


class Experiment(ExperimentCore):
    schema_checks = load_json(
        os.path.join(os.path.dirname(__file__), "../schemas/solution_checks.json")
    )

    @property
    def instance(self) -> Instance:
        return super().instance

    @property
    def solution(self) -> Solution:
        return super().solution

    @solution.setter
    def solution(self, value):
        self._solution = value

    def get_objective(self) -> float:
        return self.solution.get_assignments().values_tl().unique().len()

    def check_solution(self, *args, **kwargs) -> dict:
        # if a pair of nodes have the same colors: that's a problem
        colors = self.solution.get_assignments()
        pairs = self.instance.get_pairs()
        nodes = self.instance.get_nodes()
        missing_colors = TupList(set(nodes) - colors.keys())
        errors = [
            {"n1": n1, "n2": n2}
            for (n1, n2) in pairs
            if n1 in colors and n2 in colors and colors[n1] == colors[n2]
        ]
        return dict(pairs=errors, missing=missing_colors)

    def generate_report_quarto(self, report_name: str = "report") -> str:
        # it returns the path to the file being written

        # a user may give the full "report.qmd" name.
        # We want to take out the extension
        path_without_ext = os.path.splitext(report_name)[0]

        path_to_qmd = path_without_ext + ".qmd"
        if not os.path.exists(path_to_qmd):
            raise FileNotFoundError(f"Report with path {path_to_qmd} does not exist.")
        path_to_output = path_without_ext + ".html"
        try:
            os.remove(path_to_output)
        except FileNotFoundError:
            pass
        try:
            import quarto  # type: ignore[import-untyped]

            quarto.quarto.find_quarto()
        except FileNotFoundError:
            raise ModuleNotFoundError("Quarto is not installed.")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "experiment.json")
            # write a json with instance and solution to temp file
            self.to_json(path)
            # pass the path to the report to render
            # it generates a report with path = path_to_output
            quarto.render(input=path_to_qmd, execute_params=dict(file_name=path))
        # quarto always writes the report in the .qmd directory.
        # thus, we need to return it so the user can move it if needed
        return path_to_output

    def generate_report(self, report_name="report") -> str:
        if not os.path.isabs(report_name):
            report_name = os.path.join(
                os.path.dirname(__file__), "../report/", report_name
            )

        return self.generate_report_quarto(report_name=report_name)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            Instance.from_dict(data["instance"]),
            Solution.from_dict(data["solution"]),
        )

    def to_dict(self) -> dict:
        return dict(instance=self.instance.to_dict(), solution=self.solution.to_dict())

    @classmethod
    def from_json(cls, path: str) -> "ExperimentCore":
        with open(path, "r") as f:
            data_json = json.load(f)
        return cls.from_dict(data_json)

    def to_json(self, path: str) -> None:
        data = self.to_dict()
        with open(path, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)
