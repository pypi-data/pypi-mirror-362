from dorplan.tests.data.graph_coloring import GraphColoring
from dorplan.cli import DorPlanCli

if __name__ == "__main__":

    my_cli = DorPlanCli(GraphColoring(), None)
    my_cli.run()
