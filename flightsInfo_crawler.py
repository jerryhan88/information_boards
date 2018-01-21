import os.path as opath
from functools import reduce
import datetime, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
#
path_join = lambda prefix, name : opath.join(prefix, name)
DATA_HOME = reduce(path_join, [opath.expanduser('~'), 'Dropbox', 'Data', 'Flights'])
INTERVAL = 3600 * 3


def run():
    while True:
        today_dt = datetime.datetime.today()
        yesterday_dt = today_dt - datetime.timedelta(days=1)
        for moment, dt in [('today', today_dt), ('yesterday', yesterday_dt)]:
            dpath = opath.join(DATA_HOME, moment)
            fpath = opath.join(dpath, 'Flights-%s-%d%02d%02d.csv' % (moment, dt.year, dt.month, dt.day))
            url = 'http://www.changiairport.com/en/flight/arrivals.html?term=&schtime=&date=%s&time=all' % moment
            crawling(url, fpath)
        time.sleep(INTERVAL)


def crawling(url, fpath):
    # Start the WebDriver and load the page
    wd = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    wd.get(url)
    WebDriverWait(wd, 15).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'table')))
    # And grab the page HTML source
    html_page = wd.page_source
    wd.quit()
    # Handle html_page
    soup = BeautifulSoup(html_page)
    all_entities = soup.find_all('tr')
    with open(fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['Scheduled', 'Updated', 'From', 'Flight', 'Terminal', 'Belt', 'Status']
        writer.writerow(new_header)
    for i, row in enumerate(all_entities):
        if i < 3:
            continue
        cols = row.find_all('td')
        if len(cols) != 7:
            continue
        scheduled = cols[0].find_all(class_='visible-md')[0].get_text()
        updated = cols[1].get_text().replace('\t', '').replace('\n', '')
        dest_flights = set(e.get_text() for e in cols[2].find_all(class_="ng-binding"))
        flights = set(e.get_text() for e in cols[3].find_all(class_='ng-binding'))
        locations = dest_flights.difference(flights)
        if len(locations) == 1:
            _from = locations.pop()
        else:
            assert len(locations) == 3
            for l in locations:
                if '\nvia' in l:
                    continue
                else:
                    if l.startswith('via '):
                        via = l
                    else:
                        final = l
            _from = '%s (%s)' % (final, via)
        terminal = cols[4].find(class_='ng-binding').get_text()
        belt = cols[5].find(class_='ng-binding').get_text().replace('\n', '')
        status = cols[6].find(class_='ng-binding').get_text()
        #
        with open(fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [scheduled, updated, _from, ';'.join(flights), terminal, belt, status]
            writer.writerow(new_row)



if __name__ == '__main__':
    run()