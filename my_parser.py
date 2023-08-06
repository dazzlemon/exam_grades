import re
from bs4 import BeautifulSoup

def parse_details(details):
    subjects = {}
    matches = re.findall(r'(.+?)\s+(\d+)', details)
    for match in matches:
        subject = match[0].strip()
        score = int(match[1])
        subjects[subject] = score
    return subjects

def parse_data(html_content):
    data_list = []
    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.select('tr[class^="rstatus"]')

    for row in rows:
        attrs = {
            'name': 'ПІБ',
            'status': 'Стан',
            'priority': 'П',
            'score': 'Бал',
            'details': 'Деталізація'
        }

        for key, val in attrs.items():
            attrs[key] = row.find('td', attrs={'data-th': val}).text.strip()

        attrs['details'] = parse_details(attrs['details'])
        data_list.append(attrs)

    return data_list
