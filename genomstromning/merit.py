from .main import read_programstudents, read_course_results
import argparse
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import sys
from .version import __version__


def read_nya_merits(filename):
    pass

def setup_arguments_parser():
    parser = argparse.ArgumentParser()
    #parser.add_argument('program', help='For example NMATK, NMDVK, etc. Used to create output filename(s).')
    parser.add_argument('--version', action='version', version=f'{__version__}')
    parser.add_argument('-d', '--date', help='Give a date in ISO format (YYYY-MM-DD) so results after this date are ignored, for retrospective comparisons.')
    parser.add_argument('-t', '--title', help='Title of diagram. Without this option, a title is inferred.')
    parser.add_argument('studentfile', help='Student file')
    parser.add_argument('gradefile', help='File with "meritvärden", as exported from NyA.')
    parser.add_argument('results', nargs='+', help='Results file(s)')
    return parser.parse_args(sys.argv[1:])



def main():
    args = setup_arguments_parser()
    if args.date:
        cutoff_date = date.fromisoformat(args.date)
    else:
        cutoff_date = date.today()

    program, students = read_programstudents(args.studentfile)
    merits = read_nya_merits(args.gradefile)
    results = read_course_results(args.results, cutoff_date)
    scores = compute_scores_per_period(students, results)

    if args.title:
        create_student_bars(students, results, args.title)
    else:
        create_student_bars(students, results, program)
    
    if args.students:
        for pnr, score in sorted(scores.items(), key=lambda ps: ps[1]):
            fname = students[pnr]['Förnamn']
            lname = students[pnr]['Efternamn']
            print(f'{score:5} {fname} {lname}')

if __name__ == '__main__':
    main()
