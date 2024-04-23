import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys


def setup_arguments_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Filename for "Helårsprestationer", a CSV file.')
    parser.add_argument('-c', '--courses', help='Comma-separated list of course codes.')
    parser.add_argument('-r', '--restriction', help='Restrict to courses matching the given prefix.')
    parser.add_argument('-e', '--exclude', help='Do not include courses matching the given prefix.')
    
    return parser.parse_args(sys.argv[1:])



def read_production(filename, explicit, restriction, exclusion):
    '''
    Read report on Helårsprestationer from LADOK.

    Headers:
    Kurskod;Kurs;Omfattning;Enhet;Kod;Studietakt;Finansieringsform;Undervisningsform;Studieort;Startdatum;Kvinnor;Män;Total
    '''
    with open(filename) as h:
        lines = h.readlines()

    metadata = dict()
    for line_no, line in enumerate(lines):
        line = line.rstrip()
        tokens = line.split(';')
        if len(tokens) > 1:
            if tokens[0] == 'Kurskod':
                break
            metadata[tokens[0].strip('"')] = tokens[1].strip('"')
            
    start_line = line_no + 1    # This is where the actual data starts
    result = dict()
    for line in lines[start_line:]:
        elems = line.replace('"', '').split(';')
        course_code = elems[0]
        if is_a_keeper(course_code, explicit, restriction, exclusion):
            course_name = elems[1]
            course_credits = make_float(elems[2])
            course_event_code = elems[4]
            course_studietakt = elems[5]
            course_start_date = elems[9]
            course_hap = make_float(elems[12])
            round_info = (course_hap, course_event_code, course_studietakt, course_start_date)
            if course_code not in result:
                result[course_code] = {'name': course_name,
                                       'credits': course_credits,
                                       'rounds': [ round_info ]}
            else:
                result[course_code]['rounds'].append(round_info)

    return result, metadata


def make_float(s):
    '''
    Ensure that this string is correctly interpreted as a float.
    Swedish numbers may have a comma instead of decimal period.
    '''
    return float(s.replace(',', '.'))


def is_a_keeper(course, explicit, restriction, exclusion):
    '''
    Predicate: do we want to keep this course?
    Yes, if it matches the restriction prefix and does not match exclusion prefix.
    Yes, if it is a coures explicitly listed.
    '''
    if explicit:
        return course in explicit
    
    if exclusion:
        n = len(exclusion)
        return course[:n] != exclusion

    if restriction:
        n = len(restriction)
        return course[:n] == restriction

    return True


def list_course_production(results):
    print('# Helårsprestationer')
    for course_code, data in results.items():
        print(f'## {course_code} {data["name"]}')
        for course_round_data in sorted(data['rounds'], key=lambda x: x[3]):
            hap, event_code, _, start_date = course_round_data
            print(f'{start_date} {hap}')
        print()



def year_semester(date):
    '''
    Convert the datestring, on format YYYY-MM-DD, to semester and year, like VT23.
    '''
    year, month, day = date.split('-')
    year = str(year[2:4])
    if int(month) < 6:
        return 'VT' + year
    elif int(month) < 8:
        return 'ST' + year
    else:
        return 'HT' + year


def generate_semesters(start_year, end_year):
    '''
    Generator for elements like HT20, VT21, ST21, HT21, VT22, ...
    
    Start and end year should be given with two digits, so 23 rather than 2023.
    '''
    for year in range(start_year, end_year+1):
        for semester in ['VT', 'ST', 'HT']:
            yield semester + str(year)
        

def make_bar_diagrams_with_subplots(results, start_year, end_year):
    fig, axs = plt.subplots(len(results), sharex=True)
    fig.suptitle('HÅP-produktion')

    subfig_counter = 0
    for course_code, data in results.items():
        title = f'{course_code} {data["name"]}'
        
        production = dict()
        for data in data['rounds']:
            hap, event_code, _, start_date = data
            semester = year_semester(start_date)
            if semester in production:
                production[semester] += hap
            else:
                production[semester] = hap

        semesters = list(generate_semesters(start_year, end_year))
        hap = list(map(lambda sem: production.get(sem, 0.0), semesters))

        axs[subfig_counter].bar(semesters, hap)
        axs[subfig_counter].set_title(title, fontsize=10)
        subfig_counter += 1
    plt.savefig('tmp.pdf')
        

def make_bar_diagrams(results, start_year, end_year):
    subfig_counter = 0
    for course_code, data in results.items():
        title = f'{course_code} {data["name"]}'
        
        production = dict()
        for data in data['rounds']:
            hap, event_code, _, start_date = data
            semester = year_semester(start_date)
            if semester in production:
                production[semester] += hap
            else:
                production[semester] = hap

        semesters = list(generate_semesters(start_year, end_year))
        hap = list(map(lambda sem: production.get(sem, 0.0), semesters))

        plt.bar(semesters, hap)
        plt.title(title)
        plt.xlabel = 'Termin'
        plt.ylabel = 'HÅP'

        outfile = course_code + '.pdf'
        plt.savefig(outfile)
        print(f'Saved {outfile}', file=sys.stderr)
        plt.clf()
        

def main():
    args = setup_arguments_parser()
    explicit_courses = None
    if args.courses:
        explicit_courses = args.courses.split(',')
    results, metadata = read_production(args.infile, explicit_courses, args.restriction, args.exclude)

    period = metadata['Period']
    start_year = int(period[2:4])
    end_year = int(period[9:11])

    list_course_production(results)
    make_bar_diagrams(results, start_year, end_year)

if __name__ == '__main__':
    main()
