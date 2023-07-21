import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys
from .version import __version__


def read_programstudents(filename):
    '''
    Read student data.

    Headers:
    "Personnummer (Student)";"Förnamn (Student)";"Efternamn (Student)";"Kod (Kurspaketering)";"Benämning (Kurspaketering)";"Omf. (Kurspaketering)";"Enhet (Kurspaketering)";"Tillstånd (Sammanfattat tillstånd)";"Kod (Kurspaketeringstillfälle)";"Startdatum (Kurspaketeringstillfälle)";"Slutdatum (Kurspaketeringstillfälle)";"Studietakt (%) (Kurspaketeringstillfälle)";"Undervisningsform (Kurspaketeringstillfälle)";"Ort (Kurspaketeringstillfälle)";"Period i ordning"

    '''
    headers = ["Personnummer (Student)", "Förnamn", "Efternamn", "Programkod", "Program"]
    with open(filename, 'r') as f:
        lines = f.readlines()
    student_info = {}

    program = None
    for line in lines[:9]:
        elems = line.split(';')
        if len(elems) != 2:
            continue
        elif elems[0] == '"Utbildningskod"':
            program = elems[1].strip('"').split()[0]
    else:
        if not program:
            raise Exception('The student file is not generated the correct way. Expected a line like "Utbildningskod";"NMATK Kandidatprogram i matematik" eller liknande bland de första raderna.')

    for line in lines[9:]:
        data = line.strip().split(';')
        if len(data) < 5:
            continue
            
        pnr = data[0].strip('"')
        student_info[pnr] = dict()
        for key, val in zip(headers[1:], data[1:]):
            student_info[pnr][key] = val.strip('"')

    return program, student_info


def read_course_results(filenames):
    '''
    Read students' course results.

    Headers:
    "Personnummer (Student)";"Efternamn (Student)";"Förnamn (Student)";"Kod (Kurs)";"Benämning (Kurs)";"Omfattning (Kurs)";"Kurstillfälle (Kurs)";"Kod (Modul)";"Benämning (Modul)";"Omfattning (Modul)";"Betyg (Resultat)";"Ex. datum (Resultat)"

    '''
    headers = ['Personnummer', None, None, 'Kurskod', 'Kurs', 'Kurspoäng', 'Kurstillfälle', 'Modulkod', 'Modul', 'Modulpoäng', 'Betyg', 'Datum']
    result = {}

    for filename in filenames:
        with open(filename, 'r') as f:
            lines = f.readlines()
        for line in lines[8:]:
            data = line.strip().split(';')
            if len(data) < 5:
                continue
            
            pnr = data[0].strip('"')
            if pnr not in result:
                result[pnr] = dict()

            line = dict()
            for key, val in zip(headers[1:], data[1:]):
                if key:
                    line[key] = val.strip('"')

            kurskod = line['Kurskod']
            if kurskod not in result[pnr]:
                result[pnr][kurskod] = dict()
            if len(line['Modulkod']) > 1:
                grade = line['Betyg']
                if grade != 'F' and grade != 'FX':
                    modulkod = line['Modulkod']
                    poang = line['Modulpoäng'].replace(',', '.')
                    result[pnr][kurskod][modulkod] = float(poang)
    return result




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
    return list(sorted(codes.keys(), key=lambda code: codes[code], reverse=True))


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

    


def create_student_bars(students, results, program):
    '''
    Create bar diagrams where each bar is a student and each course adds a rectangle 
    to the bar. Sort by bar height.
    '''
    filename = program + '_per_student.pdf'
    offset = np.zeros(len(students))
    scores = compute_student_scores_per_course(students, results)
    total_scores = compute_scores_per_period(students, results)

    ranked_students = sorted(total_scores.keys(), key=lambda s: total_scores[s], reverse=True)

    index = np.arange(len(students))
    bar_width = 0.6

    style = colors_and_hatches()

    plt.clf()
    fig, ax = plt.subplots(layout='constrained')
    for course in scores:
        student_results = np.array([scores[course][pnr] for pnr in ranked_students])
        color, hatch = next(style)
        ax.barh(index, student_results, bar_width, left=offset, label=course, color=color, hatch=hatch)
        offset += student_results
    fig.legend(loc='outside right upper')
    plt.xlabel('hp')
    plt.ylabel('student (anonymt)')
    plt.title(f'{program}: Resultat per student och kurs')
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
    parser.add_argument('-s', '--students', action='store_true', help='Print student result summary to stdout')
    parser.add_argument('studentfile', help='Student file')
    parser.add_argument('results', nargs='+', help='Results file(s)')
    return parser.parse_args(sys.argv[1:])



def main():
    args = setup_arguments_parser()
    program, students = read_programstudents(args.studentfile)
    results = read_course_results(args.results)
    scores = compute_scores_per_period(students, results)

    #create_histogram(scores, args.program)
    create_student_bars(students, results, program)
    
    if args.students:
        for pnr, score in sorted(scores.items(), key=lambda ps: ps[1]):
            fname = students[pnr]['Förnamn']
            lname = students[pnr]['Efternamn']
            print(f'{score:5} {fname} {lname}')

if __name__ == '__main__':
    main()
