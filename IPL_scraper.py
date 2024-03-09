from bs4 import BeautifulSoup
import requests
import re

def fetch_page(url, is_team):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return identify_columns(soup, is_team)
        else:
            print('Website Unreachable')
            return None, None
    except requests.exceptions.RequestException as e:
        print(f'Error fetching page: {e}')
        return None, None

def extract_team_data(html_soup, headers):
    data = []
    for row in html_soup.find_all('tr'):
        cols = row.find_all('td')
        if cols:
            data.append([col.text.strip() for col in cols])
    return data, headers

def extract_player_data(html_soup, headers):
    data = []
    for row in html_soup.find_all('tr', class_='player-row'):
        cols = row.find_all('td')
        if cols:
            data.append([col.text.strip() for col in cols])
    return data, headers

def identify_columns(html_soup, is_team):
    if is_team:
        headers = [header.text.strip() for header in html_soup.find('tr').find_all('th')]
        return extract_team_data(html_soup, headers)
    else:
        headers = [header.text.strip() for header in html_soup.find('tr', class_='player-header').find_all('th')]
        return extract_player_data(html_soup, headers)
