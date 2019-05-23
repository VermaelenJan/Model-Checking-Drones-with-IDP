import argparse
import state_visualizer as vis
import model_parser as parser
from os import listdir
from os.path import isfile, join

argparser = argparse.ArgumentParser(prog='main.py', description='Visualize a specific scenario.')
available_files = [f[0:-4] for f in listdir(".\\Vis\\output models") if isfile(join(".\\Vis\\output models", f))]
argparser.add_argument('s', help='the scenario to visualize',
                       choices=available_files)


def scenario_to_filename(s):
    return "Vis/output models/" + s + ".txt"


if __name__ == "__main__":
    args = argparser.parse_args()
    scenario = scenario_to_filename(args.s)
    if scenario:
        vis.visualize(parser.generate_state(scenario))
    else:
        print("No such scenario available")
