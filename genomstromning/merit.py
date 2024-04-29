from .main import read_programstudents, read_course_results
import argparse
from datetime import date
import matplotlib.pyplot as plt
import sys
from .version import __version__
from .io import read_nya_merits, read_programstudents, read_course_results, read_personnummer
from .main import compute_scores_per_period
import logging


def plot_merits(student_scores, merits, outfileprefix='plot'):
    for merit_type in ['BI', 'BII', 'HP']:
        xvals = []
        yvals = []
        for pnr, scores in student_scores.items():
            if (pnr in merits) and (merit_type in merits[pnr]):
                xvals.append(merits[pnr][merit_type])
                yvals.append(student_scores[pnr])
        if len(xvals) == 0:
            logging.warn(f'No data for {merit_type}')
        else:
            plt.clf()
            plt.title(outfileprefix + ' ' + merit_type)
            plt.xlabel('Merit')
            plt.ylabel('hp')
            plt.plot(xvals, yvals, 'o')
            filename = outfileprefix + f'_{merit_type}.pdf'
            plt.savefig(filename)
            logging.info(f'Saved plot in {filename}')


def setup_arguments_parser():
    parser = argparse.ArgumentParser()
    #parser.add_argument('program', help='For example NMATK, NMDVK, etc. Used to create output filename(s).')
    parser.add_argument('--version', action='version', version=f'{__version__}')
    parser.add_argument('-d', '--date', help='Give a date in ISO format (YYYY-MM-DD) so results after this date are ignored, for retrospective comparisons.')
    parser.add_argument('-p', '--prefix', help='Filename prefix for plot output.')
    parser.add_argument('-s', '--studentpersonnummer', action='store_true', help='The student file is simply a list of personnummer, not a raw Ladok student file.')
    parser.add_argument('studentfile', help='File with a list of program students')
    parser.add_argument('gradefile', help='File with "meritvärden", as exported from NyA.')
    parser.add_argument('results', nargs='+', help='Results file(s)')
    return parser.parse_args(sys.argv[1:])



def main():
    args = setup_arguments_parser()
    if args.date:
        cutoff_date = date.fromisoformat(args.date)
    else:
        cutoff_date = date.today()

    if args.studentpersonnummer:
        students  = read_personnummer(args.studentfile)
    else:
        program, students = read_programstudents(args.studentfile)
    merits = read_nya_merits(args.gradefile)
    results = read_course_results(args.results, cutoff_date)
    scores = compute_scores_per_period(students, results)

    title = 'merit_plot'
    if args.prefix:
        title = args.prefix
    plot_merits(scores, merits, title)
    


if __name__ == '__main__':
    main()
