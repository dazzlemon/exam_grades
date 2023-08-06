"""Script"""
from pathlib import Path
from my_parser import parse_data
from read_fah import read_fah, FAH, TZNK, ENG
from functional import seq

grades = read_fah('grades.txt') \
    .filter(lambda r: r is not None) \
    .filter(lambda r: r['name'] != 'Сафонов Д. Є.') \
    .filter(lambda r: r['status'] != 'Скасовано (втрата пріор.)') \
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
    else:
        if parsed['details'].get(FAH) is None:
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
        else:
            actual_grades.append(parsed)

for row in parsed_data:
    if row['status'] == 'Скасовано (втрата пріор.)':
        continue
    should_append = True
    for element in grades:
        if element['name'] == row['name'] and row['status']:
            should_append = False
    if should_append:
        actual_grades.append(row)

actual_grades.sort(key=lambda x: float(x['score']), reverse=True)

i = '#'
name = 'name'
score = 'score'
status = 'status'
print(
    f'{i:>2}',
    f'{name:<20}',
    f'{score:<7}',
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
    score = row['score']
    status = row['status']
    print(
        f'{i+1:>2}',
        f'{name:<20}',
        f'{score:<7}',
        f'{status:<25}',
        row['priority'],
        f'{eng}/{tznk}/{fah}'
    )
