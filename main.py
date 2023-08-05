"""Script"""
from pathlib import Path
from functional import seq
from my_parser import parse_data

FILENAME = 'grades.txt'

# pylint: disable-next=unspecified-encoding
text = Path(FILENAME).read_text()
lines = text.splitlines()

grades = []

for line in lines:
    _, rest = line.split(' ', 1)
    lastname, rest = rest.split(' ', 1)
    firstname, rest = rest.split(' ', 1)
    patronymic, rest = rest.split(' ', 1)
    grade = rest.split()[0]
    if grade == 'н/з':
        continue
    if lastname == 'Сафонов':
        grades.append({
            'score': 183.8,
            'name': f'{lastname} {firstname[0]}. {patronymic[0]}.',
            'status': 'Waiting room',
            'priority': '1',
            'details': {
                'Іноземна мова (англійська, німецька, французька або іспанська)': 187,
                'ТЗНК': 168,
                'Фаховий іспит': 188,
            }
        })
    else:
        grades.append({
            'score': int(grade) * 0.6 + 200 * 0.4,
            'name': f'{lastname} {firstname[0]}. {patronymic[0]}.',
            'status': 'Speculative',
            'priority': '0',
            'details': {
                'Іноземна мова (англійська, німецька, французька або іспанська)': 200,
                'ТЗНК': 200,
                'Фаховий іспит': int(grade),
            }
        })

with open('list.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

parsed_data = parse_data(html_content)

def get_element_by_fullname(fullname):
    for element in parsed_data:
        if element['name'] == fullname and element['status'] != 'Скасовано (втрата пріор.)':
            return element
    return None

actual_grades = []
for row in grades:
    parsed = get_element_by_fullname(row['name'])
    if parsed is None:
        actual_grades.append(row)
    else:
        if parsed['details'].get('Фаховий іспит') is None:
            grade = float(parsed['score']) + row['details']['Фаховий іспит'] * 0.6

            actual_grades.append({
                'score': grade,
                'name': row['name'],
                'status': parsed['status'],
                'priority': parsed['priority'],
                'details': {
                    **parsed['details'],
                    'Фаховий іспит': row['details']['Фаховий іспит'],
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
    eng = row['details']['Іноземна мова (англійська, німецька, французька або іспанська)']
    tznk = row['details']['ТЗНК']
    fah = row['details'].get('Фаховий іспит')
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
