# d-OR-plan

Desktop OR Planner. A desktop wrapper for applications based on the Cornflow-client format. Check out the [Cornflow project](https://github.com/baobabsoluciones/cornflow).
[Here is a guide](https://baobabsoluciones.github.io/cornflow/guides/deploy_solver_new.html) on how to configure an app in the right format.

Another option is just to check the tests/data/graph_coloring example that comes inside this project. 

## Installation

Running uv or pip should work:

Using uv:

```
uv install dorplan[example]
```

If reports are required, install the reports dependencies:

```
uv install dorplan[example, reports]
```

In the case of Windows, you will also need to install quarto separately. You can find the instructions [here](https://quarto.org/docs/download/).

This is until the quarto team fixes this issue: https://github.com/quarto-dev/quarto-cli/issues/12314

Using pip

```
python -m pip install dorplan[example]
```

## Testing

If you want to test the example app, run:

```
uv run dorplan/example/example.py
```

The example shows a graph-coloring problem, which is a simple optimization problem where the goal is to color the nodes using the least number of colors in a graph such that no two adjacent nodes have the same color.

Many engines are available to solve this problem, such as [CP-SAT](https://developers.google.com/optimization/cp), and [HiGHS](https://github.com/ERGO-Code/HiGHS) [via PuLP](https://github.com/coin-or/pulp/), [networkX](https://networkx.org/), and [timefold](https://timefold.ai/). For those that take a time limit (all but networkx), you can set it in the GUI. You can also stop the execution if the solver is configured to do it (all but networkx).

## Functionality

* Import and export data (in json format and Excel).
* Load example data.
* Solve an instance.
* Show interactive logs in the GUI.
* Stop a running solver, if the correct callback is implemented.
* Kill a running solver, if the correct worker is selected.
* Generate a report, if a quarto report is available.
* Open the report in a new browser tab.

## How to run it

In its simplest form, you can just pass it the Cornflow `ApplicationCore` class and the initialized options for the solver. More information on how to create a Cornflow-compatible Application [here](https://baobabsoluciones.github.io/cornflow/guides/deploy_solver_new.html#application-class). Alternatively, check the example in `dorplan/tests/data/graph_coloring/__init__.py`

The app will be opened in a new window, and you can interact with it.

```python
from dorplan.app import DorPlan
from dorplan.tests.data.graph_coloring import GraphColoring

app = DorPlan(GraphColoring, {})

```

## Functionality

It's possible to load one of the test cases from the app

![](dorplan/example/img/test_cases.png)

After setting a time limit, you can solve the instance by clicking on "Generate plan" and look at the progress in the GUI. 
You can also stop the execution (if the solver is configured to do it).

![](dorplan/example/img/output_log.png)

You can generate a report if the solver has a Quarto report available and you installed the `reports` dependencies.

![](dorplan/example/img/report_log.png)

The report will then appear on the screen (with terrible format).

![report](dorplan/example/img/report.png)

But you can always open it in a new browser tab by clicking the "Open report" button.

![report](dorplan/example/img/report_html.png)