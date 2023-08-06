"""Script"""
from pathlib import Path
from my_parser import parse_data
from read_fah import read_fah, FAH, TZNK, ENG
from functional import seq

grades = read_fah('grades.txt') \
    .filter(lambda r: r is not None) \
    .filter(lambda r: r['name'] != 'Сафонов Д. Є.') \
    .list()

grades.append({
    'score': 183.8,
    'name': 'Сафонов Д. Є.',
    'status': 'Waiting room',
    'priority': '1',
    'details': {
        ENG: 187,
        TZNK: 168,
        FAH: 188,
    }
})

html_content = Path('list.html').read_text()
parsed_data = parse_data(html_content)

actual_grades = []
for row in grades:
    parsed = seq(parsed_data).find(lambda r: r['name'] == row['name'])
    if parsed is None:
        actual_grades.append(row)
        continue

    if parsed['details'].get(FAH) is not None:
        actual_grades.append(parsed)
        continue

    grade = float(parsed['score']) + row['details'][FAH] * 0.6

    actual_grades.append({
        'score': grade,
        'name': row['name'],
        'status': parsed['status'],
        'priority': parsed['priority'],
        'details': {
            **parsed['details'],
            FAH: row['details'][FAH],
        }
    })

actual_grades = seq(actual_grades) \
    .where(lambda r: r['status'] != 'Скасовано (втрата пріор.)') \
    .where(lambda r: r['priority'] != 'К') \
    .sorted(key=lambda x: float(x['score']), reverse=True) \
    .list()

i = '#'
name = 'name'
score = 'score'
status = 'status'
print(
    f'{i:>2}',
    f'{name:<20}',
    f'{score:<5}',
    f'{status:<25}',
    'p',
    'eng/tznk/fah'
)
print('')
for i, row in enumerate(actual_grades):
    details = row['details']
    eng = details[ENG]
    tznk = details[TZNK]
    fah = details.get(FAH)

    name = row['name']
    score = float(row['score'])
    status = row['status']
    print(
        f'{i+1:>2}',
        f'{name:<20}',
        f'{score:<5}',
        f'{status:<25}',
        row['priority'],
        f'{eng}/{tznk}/{fah}'
    )
