from functional import seq
from read_fah import FAH

def merge(parsed_data, fah):
    actual_grades = []
    for parsed in parsed_data:
        if parsed.get(FAH) is not None:
            actual_grades.append(parsed)
            continue

        fah_record = seq(fah).find(lambda r: r['name'] == parsed['name'])
        if fah_record is None:
            actual_grades.append({
                **parsed,
                FAH: 0
            })
            continue

        actual_grades.append({
            **parsed,
            FAH: fah_record[FAH]
        })

    for row in fah:
        parsed = seq(parsed_data).find(lambda r: r['name'] == row['name'])
        if parsed is None:
            actual_grades.append(row)
    return actual_grades
