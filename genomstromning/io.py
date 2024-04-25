from datetime import date
import re

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
        elif elems[0] == '"Utbildningskod"' or elems[0] == '"Utbildning"':
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


def read_course_results(filenames, cutoff_date=date.today()):
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

            if 'Datum' in line:
                res_date = date.fromisoformat(line['Datum'])
                if res_date > cutoff_date: # We ignore later results
                    continue

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


bi =  re.compile('BI\\s+\\((\\d+\\.\\d+)\\)')
bii = re.compile('BII\\s+\\((\\d+\\.\\d+)\\)')
hp =  re.compile('HP\\s+\\((\\d+\\.\\d+)\\)')


def parse_merits(meritstring):
    data = {}
    m_bi = bi.search(meritstring)
    m_bii = bii.search(meritstring)
    m_hp = hp.search(meritstring)
    if m_bi:
        data['BI'] = float(m_bi.group(1))
    if m_bii:
        data['BII'] = float(m_bii.group(1))
    if m_hp:
        data['HP'] = float(m_hp.group(1))
    return data


def read_nya_merits(filename):
    merits = {}
    with open(filename) as h:
        for line in h:
            pnr, enamn, fnamn, program, prio, _, meritstring, _, _ = line.split(';')
            merits[pnr] = parse_merits(meritstring)
    return merits


def read_personnummer(filename):
    '''
    Read a simple file containing one personnummer per line.
    Return a dict with personnummer as keys and no value.
    '''
    personnummer = {}
    with open(filename) as h:
        for line in h:
            line = line.strip()
            if len(line) > 0:
                personnummer[line] = True
    if len(personnummer) == 0:
        logging.error(f'No data in {filename} that can be read as personnummer')
    return personnummer
