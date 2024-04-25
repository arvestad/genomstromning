import argparse

from .version import __version__
import .genomstromning as g


def sort_courses(


def setup_arg_parser():
    parser.add_argument('--version', action='version', version=f'{__version__}')
    parser.add_argument('-c', '--courses', help='List course codes as a comma-separated string. Eg.: "MM2001,DA2004"')
    parser.add_argument('-m', '--min_production', type=float, help='Only output courses that have produced at least this many HÅP')
    parser.add_argument('results', nargs='+', help='Results file(s)')
    return parser.parse_args(sys.argv[1:])


def production():
    args = setup_arg_parser()
    results = g.read_course_results(args.results)
    courses = sort_courses(results)



