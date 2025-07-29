import click
import os
import functools
from cornflow_client import ExperimentCore, ApplicationCore
import shutil


input_file_format = click.Path(
    exists=True, dir_okay=False, file_okay=True, readable=True
)


class DorPlanCli(object):
    def __init__(self, my_app: ApplicationCore, my_engine: ExperimentCore | None):
        self.app = my_app
        self.engine = my_engine

    def run(self):
        """Run the CLI application."""
        cli(obj=self)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(DorPlanCli)


def common_options(f):
    @click.option(
        "--instance",
        default=None,
        help="Input path (.json).",
        type=input_file_format,
    )
    @click.option(
        "--solution",
        help="Solution path (.json).",
        default=None,
        type=input_file_format,
    )
    @click.option(
        "--excel", default=None, help="Dataset (.xlsx).", type=input_file_format
    )
    @click.option(
        "--config",
        "-c",
        "config",
        help="Optional configuration for solver.",
        default=None,
        type=(str, str),
        multiple=True,
    )
    @click.option("--test", help="Run test instance.", default=False, is_flag=True)
    @click.option("--report-path", help="Report path.", default="report.html")
    @functools.wraps(f)
    def wrapper_common_options(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper_common_options


@cli.command()
@common_options
@click.option("--output-path", "-o", help="Output path.", default="solution")
@click.pass_context
def solve_instance(
    ctx,
    instance: os.PathLike,
    solution: os.PathLike,
    excel: os.PathLike,
    config: dict,
    test: bool,
    report_path,
    output_path,
):
    """Solves an optimization problem."""
    app = ctx.obj
    instance, solution = get_instance_solution(instance, solution, excel, test, app)
    if excel:
        extension = ".xlsx"
    else:
        extension = ".json"
    if config is None:
        config = {}
    else:
        config = dict(config)
    if "solver" in config:
        engine = app.app.get_solver(config["solver"])
    elif app.engine is not None:
        engine = app.engine
    else:
        raise ValueError(
            "No solver provided. Please provide a solver in the configuration."
        )
    if "timeLimit" in config:
        config["timeLimit"] = int(config["timeLimit"])

    filename, ext = os.path.splitext(output_path)
    if ext != extension:
        output_path = filename + extension

    experiment = engine.from_dict(dict(instance=instance, solution=solution))
    experiment.solve(config)

    if not experiment.solution:
        return print("No solution found.")

    print("Solution:")

    if extension == ".json":
        experiment.solution.to_json(output_path)
    elif extension == ".xlsx":
        experiment.to_excel(output_path)
    print(f"Solution saved in {output_path}")
    if config is not None:
        report_name = config.get("report", {}).get("name")
        if report_name is not None:
            curr_path = experiment.generate_report(report_name)
            os.rename(curr_path, report_path)
            print(f"Report saved in {report_path}")
    return


@cli.command()
@common_options
@click.pass_context
def get_report(ctx, instance, solution, excel, config, test, report_path):
    """Generates a report for the problem."""
    app = ctx.obj
    instance, solution = get_instance_solution(instance, solution, excel, test, app)

    if app.engine is None and "solver" not in config:
        raise ValueError(
            "No solver provided. Please provide a solver in the configuration."
        )

    experiment = app.engine.from_dict(dict(instance=instance, solution=solution))
    print("Starting to write the report")
    if config is None:
        report_name = "report"
    else:
        config = dict(config)
        report_name = config.get("report", {}).get("name", "report")
    curr_path = experiment.generate_report(report_name)
    if os.path.isdir(report_path):
        report_path = os.path.join(report_path, "report.html")

    shutil.move(curr_path, report_path)
    print(f"Report saved in {report_path}")


def get_instance_solution(
    instance_path: os.PathLike | str | None,
    solution_path: os.PathLike | str | None,
    excel,
    test,
    app: DorPlanCli,
):
    Instance = app.app.instance
    Solution = app.app.solution
    test_cases = app.app.test_cases
    solution, instance = None, None
    if excel:
        if instance_path or solution_path or test:
            raise ValueError(
                "You can't provide an instance or solution or a test with an excel file."
            )
        instance = Instance.from_excel(excel).to_dict()
        try:
            solution = Solution.from_excel(excel).to_dict()
        except:
            # TODO: find out which exception is raised when there is no solution sheet.
            solution = None
    else:
        # We load the instance.
        if instance_path:
            instance = Instance.from_json(instance_path).to_dict()
        # If a solution is provided, we load it.
        if solution_path:
            solution = Solution.from_json(solution_path).to_dict()

    if test:
        if instance_path:
            raise ValueError("You can't provide a test flag and an instance.")
        if len(test_cases) == 0:
            raise ValueError("No test cases found.")
        instance = test_cases[0]["instance"]
        solution = test_cases[0].get("solution")

    if instance is None:
        raise ValueError(
            "No instance was provided. Please provide an instance to solve."
        )
    return instance, solution
