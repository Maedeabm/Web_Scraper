from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
from PyInquirer import prompt
import os
import signal
import sys


def handle_error():
    print('Ctrl+C was pressed!')
    terminate_program()


def terminate_program():
    print('Program is terminating')
    sys.exit(0)


def signal_handler(sig, frame):
    handle_error()


signal.signal(signal.SIGINT, signal_handler)


def store_data(data, headers, dataset_name, filename):
    dataframe = pd.DataFrame(data, columns=headers)
    filepath = './' + filename + '-' + dataset_name + '.csv'
    dataframe.to_csv(filepath, index=False)
    print(dataset_name + ' stored as: ' + os.path.dirname(os.path.abspath(__file__)) + '/' + dataset_name + '.csv')


def extract_team_data(html_soup, headers):
    extracted_data = []
    for cell in html_soup.find_all('td'):
        extracted_data.append(re.sub(r'\n[\s]*', " ", cell.get_text().strip()))
    extracted_data = np.array(extracted_data).reshape(len(extracted_data) // len(headers), len(headers) + 1)
    extracted_data = np.delete(extracted_data, 0, axis=1)
    return extracted_data, headers


def extract_player_data(html_soup, headers):
    extracted_data = []
    for cell in html_soup.find_all('td', class_=re.compile(r'top-players*')):
        extracted_data.append(re.sub(r'\n[\s]*', " ", cell.get_text().strip()))
    extracted_data = np.array(extracted_data).reshape(len(extracted_data) // len(headers), len(headers))
    return extracted_data, headers


def identify_columns(html_soup, is_team):
    try:
        if is_team:
            headers = list(filter(None, html_soup.find('tr', class_='standings-table__header').get_text().split('\n')))
            return extract_team_data(html_soup, headers)
        else:
            headers = re.sub(r'\n[\s]*', '\n',
                             html_soup.find('tr', class_=re.compile(r'top-players__header*')).get_text()).strip().split('\n')
            return extract_player_data(html_soup, headers)
    except AttributeError:
        return [], []


def scrape_data(years, stats):
    base_url = 'https://www.iplt20.com/stats/'
    base_filename = 'Result'
    for year in years:
        for stat in stats:
            if stat == 'team-ranking':
                url = base_url + year
                data, headers = fetch_page(url, True)
                dataset_name = 'Team-Ranking-' + year
            else:
                url = base_url + year + '/' + stat
                data, headers = fetch_page(url, False)
                dataset_name = str.title(stat) + '-' + year
            if len(data) == 0:
                print(dataset_name + ' :' + 'Data not Available')
            else:
                store_data(data, headers, dataset_name, base_filename)


def fetch_page(url, is_team):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_soup = BeautifulSoup(response.content, 'html.parser')
            data, headers = identify_columns(html_soup, is_team)
            return data, headers
        else:
            print('Website Unreachable')
            return
    except requests.exceptions.ConnectionError:
        print('Please check network connection')
        return


def extract_years(html_soup):
    years_list = [year.get_text() for year in html_soup.find_all('a', class_=re.compile(r'sub-menu*'))]
    years_list[-1] = 'all-time'
    return years_list


def extract_stats(html_soup):
    stats_elements = html_soup.find_all('a', class_=re.compile(r'side*'))
    stats_urls = [re.search(r'\d/(.*)', stat['href']).group(1) for stat in stats_elements]
    stats_titles = [re.sub(r'[\n]+', '\n', stat.get_text()).strip() for stat in stats_elements]
    return stats_urls, stats_titles


def get_year_and_stats():
    url = 'https://www.iplt20.com/stats/2019'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_soup = BeautifulSoup(response.content, 'html.parser')
            years = extract_years(html_soup)
            stats_urls, stats_titles = extract_stats(html_soup)
            stats_urls.append('team-ranking')
            stats_titles.append('Team Ranking')
            return years, stats_urls, stats_titles
    except requests.exceptions.ConnectionError:
        print('Please check network connection')
        return [], [], []


def setup_questions(years, stats_titles, stats_urls):
    year_options = [{'name': year} for year in years]
    stat_options = [{'name': stats_titles[i], 'value': stats_urls[i]} for i in range(len(stats_titles))]
    return year_options, stat_options


def get_user_input(years_options, stats_options):
    user_selection = {'years': '', 'stats': ''}
    try:
        while len(user_selection.get('years')) == 0 or len(user_selection.get('stats')) == 0:
            questions = [
                {
                    'type': 'checkbox',
                    'message': 'Select years',
                    'name': 'years',
                    'choices': years_options,
                }, {
                    'type': 'checkbox',
                    'message': 'Select statistics',
                    'name': 'stats',
                    'choices': stats_options,
                }
            ]
            user_selection = prompt(questions)
    except TypeError:
        handle_error()
    except EOFError:
        terminate_program()
    return user_selection['years'], user_selection['stats']


def main():
    years, stats_urls, stats_titles = get_year_and_stats()
    years_options, stats_options = setup_questions(years, stats_titles, stats_urls)
    selected_years, selected_stats = get_user_input(years_options, stats_options)
    print('Collecting and saving data.')
    scrape_data(selected_years, selected_stats)


if __name__ == '__main__':
    try:
        main()
    except AssertionError:
        print('Interface not supported, please use terminal or command prompt.')
