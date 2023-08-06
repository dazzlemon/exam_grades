from read_fah import FAH, TZNK, ENG

def print_row(i, name, score, status, priority, eng, tznk, fah):
    print(
        f'{i:>2}',
        f'{name:<20}',
        f'{score:<5}',
        f'{status:<25}',
        priority,
        f'{eng}/{tznk}/{fah}'
    )

def print_rows(rows):
    for i, row in enumerate(rows):
        print_row(
            i+1,
            row['name'],
            row['score'],
            row['status'],
            row['priority'],
            row.get(ENG),
            row.get(TZNK),
            row.get(FAH),
        )