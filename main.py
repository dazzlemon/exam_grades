"""Script"""
from pathlib import Path
from functional import seq
from my_parser import parse_data
from read_fah import read_fah, FAH, TZNK, ENG
from merge import merge
from printer import print_row, print_rows

grades = read_fah('grades.txt') \
    .filter(lambda r: r is not None) \
    .filter(lambda r: r['name'] != 'Сафонов Д. Є.') \
    .list()

grades.append({
    'name': 'Сафонов Д. Є.',
    'status': 'Waiting room',
    'priority': '1',
    ENG: 187,
    TZNK: 168,
    FAH: 188,
})

html_content = Path('list.html').read_text()
parsed_data = parse_data(html_content)

grades = merge(parsed_data, grades)

actual_grades = seq(grades) \
    .where(lambda r: r['status'] != 'Скасовано (втрата пріор.)') \
    .where(lambda r: r['priority'] != 'К') \
    .where(lambda r: r[FAH] != 0) \
    .map(lambda r: {
        **r,
        'score': round( r[FAH] * 0.6
                      + r[ENG] * 0.2
                      + r[TZNK] * 0.2, 1)
    }) \
    .sorted(key=lambda x: float(x['score']), reverse=True) \
    .list()

print_row('#', 'name', 'score', 'status', 'p', 'eng', 'tznk', 'fah')
print('')
print_rows(actual_grades)

invalid_grades = seq(grades) \
    .where(lambda r: r['status'] == 'Скасовано (втрата пріор.)'
                  or r['priority'] == 'К'
                  or r[FAH] == 0) \
    .map(lambda r: {
        **r,
        'status': r['status'] if r['status'] != 'Speculative' else 'invalid fah',
        'score': 0
    }) \
    .sorted(key=lambda x: float(x['score']), reverse=True) \
    .list()

print('\ninvalid\n')
print_rows(invalid_grades)
