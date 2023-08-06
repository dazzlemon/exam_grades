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
        # Extract individual data fields
        full_name = row.find('td', attrs={'data-th': 'ПІБ'}).text.strip()
        status = row.find('td', attrs={'data-th': 'Стан'}).text.strip()
        priority = row.find('td', attrs={'data-th': 'П'}).text.strip()
        score = row.find('td', attrs={'data-th': 'Бал'}).text.strip()
        details = row.find('td', attrs={'data-th': 'Деталізація'}).text.strip()

        # Parse the details and extract subjects with scores
        parsed_details = parse_details(details)

        # Append the extracted data as a dictionary to the list
        data_list.append({
            'name': full_name,
            'status': status,
            'priority': priority,
            'score': score,
            'details': parsed_details
        })

    return data_list
