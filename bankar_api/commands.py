import os
import sys
import click

from .models import StateModel


@click.argument("csv_file", type=click.STRING)
def import_states(csv_file=None):
    "Import states from a csv file"
    if csv_file is None:
        csv_file = 'states.csv'
    csv_file = os.path.abspath(csv_file)
    if not os.path.isfile(csv_file):
        print("The file '{}' does not exist.".format(csv_file))
        sys.exit(2)
    print("Importing states from file '{}'...".format(csv_file))
    with open(csv_file) as stream:
        StateModel.import_csv(stream)
    print("States imported.")
