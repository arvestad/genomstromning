import argparse
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import sys
from .version import __version__
from .io import read_programstudents, read_course_results




def compute_scores_per_period(students, results):
    '''
    For each student, report the number of points managed during the implicitly defined period.
    '''
    scores = {}
    for pnr in students:
        sc = 0
        if pnr in results:
            if pnr not in scores:
                scores[pnr] = 0                
            for res in results[pnr]:
                for module in results[pnr][res]:
                    scores[pnr] += results[pnr][res][module]
        else:
            scores[pnr] = 0
    return scores


def get_course_codes(students, results):
    '''
    Return a list of course codes, sorted by the order of total hp generated.
    This should place MM2001 first, but it is discovered in the data.
    '''
    codes = dict()
    for pnr, res in results.items():
        for code in res:
            if code not in codes:
                codes[code] = 0
            for module, hp in res[code].items():
                if pnr in students:
                    codes[code] += hp

    sorted_codes = sorted(codes.keys(), key=lambda code: codes[code], reverse=True)
    non_zero_credits = filter(lambda code: codes[code] > 0, sorted_codes)
    return list(non_zero_credits)


def compute_student_scores_per_course(students, results):
    student_scores = {}
    codes = get_course_codes(students, results)

    scores = dict()             # Map course code to student points
    for code in codes:
        scores[code] = dict()
        for pnr in students:
            sc = 0
            if pnr in results and code in results[pnr]:
                for module in results[pnr][code]:
                    sc += results[pnr][code][module]
            scores[code][pnr] = sc
    return scores
        

def colors_and_hatches():
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']    

    hatches = [' ', '//', '\\\\', '+']

    for hatch in hatches:
        for color in colors:
            yield color, hatch

course_color_and_hatch = {
    'MM2001': ('#1f77b4', ' '),
    'MM2003': ('#1f77b4', '**'),
    'MM5012': ('#ff7f0e', ' '),
    'DA2004': ('#2ca02c', ' '),
    'DA2005': ('#2ca02c', ' '),
    'MM5013': ('#d62728', ' '),
    'DA3018': ('#9467bd', '**'),
    'DA4006': ('#9467bd', ' '),
    'MM5016': ('#8c564b', ' '),
    'MM5010': ('#e377c2', ' '),
    'MM5011': ('#e377c2', '//'),
    'MM5015': ('#1f77b4', '//'),
    'MT3001': ('#7f7f7f', ' '),
    'MT4001': ('#bcbd22', ' '),
    'MT4007': ('#17becf', ' '),
}
available = [
    '#1f77b4',
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf'        
]

def colors_and_hatches_by_course(code):

    if code in course_color_and_hatch:
        return course_color_and_hatch[code]
    else:
        print(f'Added color for {code}', file=sys.stderr)
        color = available.pop()
        hatch = '\\\\'
        course_color_and_hatch[code] = (color, hatch)
        return color, hatch    


def create_student_bars(students, results, title):
    '''
    Create bar diagrams where each bar is a student and each course adds a rectangle 
    to the bar. Sort by bar height.
    '''
    filename = title + '_per_student.pdf'
    offset = np.zeros(len(students))
    scores = compute_student_scores_per_course(students, results)
    total_scores = compute_scores_per_period(students, results)

    ranked_students = sorted(total_scores.keys(), key=lambda s: total_scores[s], reverse=True)

    index = np.arange(len(students))
    bar_width = 0.6

    #style = colors_and_hatches()

    plt.clf()
    fig, ax = plt.subplots(layout='constrained')
    for course in scores:
        student_results = np.array([scores[course][pnr] for pnr in ranked_students])
        #color, hatch = next(style)
        color, hatch = colors_and_hatches_by_course(course)
        ax.barh(index, student_results, bar_width, left=offset, label=course, color=color, hatch=hatch)
        offset += student_results
    fig.legend(loc='outside right upper')
    plt.xlabel('hp')
    plt.ylabel('student (anonymt)')
    plt.title(f'{title}: Resultat per student och kurs')
    plt.savefig(filename)


def create_histogram(data_dict, program):
    '''
    Create a histogram of the values in the dict (ignoring the keys) 
    and save a the histogram in the filename (should end in ".pdf").
    '''
    filename = program + '_hp_per_year.pdf'
    values = data_dict.values()
    plt.hist(values, bins=10, range=(0, max(values)))  # adjust the number of bins as needed
    plt.xlim = max(values)
    plt.xlabel('hp')
    plt.ylabel('Antal')
    plt.title(f'{program}: fördelning av hp')
    plt.savefig(filename)


def setup_arguments_parser():
    parser = argparse.ArgumentParser()
    #parser.add_argument('program', help='For example NMATK, NMDVK, etc. Used to create output filename(s).')
    parser.add_argument('--version', action='version', version=f'{__version__}')
    parser.add_argument('-d', '--date', help='Give a date in ISO format (YYYY-MM-DD) so results after this date are ignored, for retrospective comparisons.')
    parser.add_argument('-s', '--students', action='store_true', help='Print student result summary to stdout')
    parser.add_argument('-t', '--title', help='Title of diagram. Without this option, a title is inferred.')
    parser.add_argument('studentfile', help='Student file')
    parser.add_argument('results', nargs='+', help='Results file(s)')
    return parser.parse_args(sys.argv[1:])



def main():
    args = setup_arguments_parser()
    if args.date:
        cutoff_date = date.fromisoformat(args.date)
    else:
        cutoff_date = date.today()

    program, students = read_programstudents(args.studentfile)
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
