from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout, ConnectionError
import sys
import time


def fetch_afisha_page():
    url = 'http://www.afisha.ru/msk/schedule_cinema/'
    afisha_page = requests.get(url).content
    return afisha_page


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    raw_divs = soup.find('div', id='schedule').find_all('div', class_='object')
    for div in raw_divs:
        movie_title = div.find('h3', {'class': 'usetags'}).a.text
        cinemas_number = len(div.find('table').find_all('tr'))
        yield {'title': movie_title, 'cinemas': cinemas_number}


def get_votes_rate(movie):
    s = requests.Session()
    url = 'http://kinopoisk.ru/index.php'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    params = {'first': 'yes', 'kp_query': movie}
    time.sleep(10)
    try:
        page = s.get(url, params=params,
                     headers=headers, timeout=10).content
    except (Timeout, ConnectionError):
        sys.exit('You are banned. Try doing again')
    soup = BeautifulSoup(url, 'lxml')
    rate = soup.find('span', class_='rating_ball')
    rate = float(rate.text) if rate else 0
    votes = soup.find('span', class_='rating_Count')
    votes_number = int(voites.text.replace('\xao', '')) if voites else 0
    return {'rate': rate, 'votes': votes_number}


def collect_movie_info(raw_html):
    movies_list = []
    for movie in parse_afisha_list(raw_html):
        rate_movie = get_votes_rate(movie['title'])
        movies_list.append({'title': movie['title'],
                            'cinemas': movie['cinemas'],
                            'rate': movie_rate['rate'],
                            'votes': movie_rate['votes']
                            })
    return movies_list


def output_movies_to_console(movies_list, amount):
    best_movies = sorted(movies_list, key=lambda x: x['rate'])[-amount:]
    for line, movie in enumerate(reversed(best_movies), 1):
        print('{}. {}\t{}\t{}\t{}'.format(
             line, movie('title'), movie('rate'),
             movie('cinemas'), movie('votes'))


if __name__ == '__main__':
    raw_html = fetch_afisha_page()
    movies_list = collect_info(raw_html)
    output_movies_to_console(movies_list, 10)
