from functional import seq
from read_fah import read_fah, FAH, TZNK, ENG

def merge(parsed_data, fah):
    actual_grades = []
    for row in fah:
        parsed = seq(parsed_data).find(lambda r: r['name'] == row['name'])
        if parsed is None:
            actual_grades.append(row)
            continue
    
        if parsed['details'].get(FAH) is not None:
            actual_grades.append(parsed)
            continue
    
        grade = float(parsed['score']) + row['details'][FAH] * 0.6
    
        actual_grades.append({
            **parsed,
            'score': grade,
            'details': {
                **parsed['details'],
                FAH: row['details'][FAH],
            }
        })
    return actual_grades
