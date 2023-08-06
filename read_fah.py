from pathlib import Path
from functional import seq

ENG = 'Іноземна мова (англійська, німецька, французька або іспанська)'
TZNK = 'ТЗНК'
FAH = 'Фаховий іспит'

def line_to_record(line):
    _, rest = line.split(' ', 1)
    lastname, rest = rest.split(' ', 1)
    firstname, rest = rest.split(' ', 1)
    patronymic, rest = rest.split(' ', 1)
    grade = rest.split()[0]

    if grade == 'н/з':
        return None

    return {
        'name': f'{lastname} {firstname[0]}. {patronymic[0]}.',
        'status': 'Speculative',
        'priority': '0',
        ENG: 200,
        TZNK: 200,
        FAH: int(grade),
    }

def read_fah(filename):
    # pylint: disable-next=unspecified-encoding
    lines = Path(filename).read_text().splitlines()
    return seq(lines) \
        .map(line_to_record) \
        .filter(lambda r: r is not None)
