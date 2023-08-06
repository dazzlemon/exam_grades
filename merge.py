from functional import seq
from read_fah import FAH

def merge(parsed_data, fah):
    actual_grades = []
    for row in fah:
        parsed = seq(parsed_data).find(lambda r: r['name'] == row['name'])
        if parsed is None:
            actual_grades.append(row)
            continue
    
        if parsed.get(FAH) is not None:
            actual_grades.append(parsed)
            continue
    
        actual_grades.append({
            **parsed,
            FAH: row[FAH],
        })
    return actual_grades
