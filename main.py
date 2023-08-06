"""Script"""
from pathlib import Path
from functional import seq
from my_parser import parse_data
from read_fah import read_fah, FAH, TZNK, ENG
from merge import merge

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

actual_grades = merge(parsed_data, grades)

actual_grades = seq(actual_grades) \
    .where(lambda r: r['status'] != 'Скасовано (втрата пріор.)') \
    .where(lambda r: r['priority'] != 'К') \
    .map(lambda r: {
        **r,
        'score': round( r[FAH] * 0.6
                      + r[ENG] * 0.2
                      + r[TZNK] * 0.2, 1)
    }) \
    .sorted(key=lambda x: float(x['score']), reverse=True) \
    .list()

def print_row(i, name, score, status, priority, eng, tznk, fah):
    print(
        f'{i:>2}',
        f'{name:<20}',
        f'{score:<5}',
        f'{status:<25}',
        priority,
        f'{eng}/{tznk}/{fah}'
    )

print_row('#', 'name', 'score', 'status', 'p', 'eng', 'tznk', 'fah')
print('')
for i, row in enumerate(actual_grades):
    print_row(
        i+1,
        row['name'],
        row['score'],
        row['status'],
        row['priority'],
        row[ENG],
        row[TZNK],
        row[FAH],
    )
