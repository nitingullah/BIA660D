"""
    Took assistance from Souravi Sudame
"""



import random
import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup


def write_to_csv(q_num, column_names, ltd):
    with open('Question_question%s.csv' % q_num, 'w') as f:
        csv_obj = csv.DictWriter(f, column_names)
        csv_obj.writerows(ltd)


def most_home_runs():
    driver = webdriver.Chrome('../../chromedriver')

    driver.get(
        "http://mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='S'&season=2018&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=1&ts=1520478568794")

    time.sleep(7)

    driver.find_element_by_xpath('//*[@id="sp_hitting-0"]/fieldset[1]').click()

    time.sleep(random.randint(10, 20))

    driver.find_element_by_xpath('//*[@id="sp_hitting_season"]/option[4]').click()

    time.sleep(random.randint(10, 15))

    driver.find_element_by_xpath('//*[@id="top_nav"]/div/ul/li[5]').click()

    time.sleep(random.randint(10, 15))

    driver.find_element_by_xpath('//*[@id="st_hitting_game_type"]').click()

    time.sleep(random.randint(10, 15))

    driver.find_element_by_xpath('//*[@id="st_hitting_game_type"]/option[1]').click()

    root = driver.page_source

    soup = BeautifulSoup(root, 'html.parser')

    m_hr = []
    for tr in soup.find_all('table')[0].find('tbody'):
        m_hr.append({'team': tr.find('td', {'index': 1}).get_text(),
                     'league': tr.find('td', {'index': 3}).get_text(),
                     'HR': tr.find('td', {'index': 10}).get_text()})

    write_to_csv('1', ['team', 'league', 'HR'], m_hr)
    # answer 1
    print(sorted(m_hr, key=lambda x: x['HR'])[-1]['team'])

    al_list = [int(i['HR']) for i in filter(lambda x: x['league'] == 'AL', m_hr)]
    nl_list = [int(i['HR']) for i in filter(lambda x: x['league'] == 'NL', m_hr)]

    # answer 2a
    print('Answer 2a')
    if sum(al_list) / len(al_list) > sum(nl_list) / len(nl_list):
        print('AL ' + str(sum(al_list) / len(al_list)))
    else:
        print('NL ' + str(sum(al_list) / len(al_list)))
    write_to_csv('2a', ['team', 'league', 'HR'], m_hr)
    select_element = driver.find_element_by_xpath('//*[@id="st_hitting_hitting_splits"]')
    select_element.click()

    time.sleep(random.randint(1, 5))

    select_element.find_element_by_xpath('//*[@id="st_hitting_hitting_splits"]/optgroup[12]/option[1]').click()

    time.sleep(random.randint(1, 5))

    soup_first_innings = BeautifulSoup(driver.page_source, 'html.parser')

    fi_hr = []

    for tr in soup_first_innings.find_all('table')[0].find('tbody'):
        fi_hr.append({'team': tr.find('td', {'index': 1}).get_text(),
                      'league': tr.find('td', {'index': 3}).get_text(),
                      'HR': tr.find('td', {'index': 10}).get_text()})

    write_to_csv('2b', ['team', 'league', 'HR'], fi_hr)

    fal_list = [int(i['HR']) for i in filter(lambda x: x['league'] == 'AL', fi_hr)]
    fnl_list = [int(i['HR']) for i in filter(lambda x: x['league'] == 'NL', fi_hr)]

    # answer 2b
    print('Answer 2b')
    if sum(fal_list) / len(fal_list) > sum(fnl_list) / len(fnl_list):
        print('AL ' + str(sum(fal_list) / len(fal_list)))
    else:
        print('NL ' + str(sum(fal_list) / len(fal_list)))

    time.sleep(random.randint(1, 5))
    se_player = driver.find_element_by_xpath('//*[@id="top_nav"]')

    # click player
    se_player.find_element_by_xpath('//*[@id="sp_parent"]').click()

    time.sleep(random.randint(1, 5))

    # click year drop down
    se_player.find_element_by_xpath('//*[@id="sp_hitting_season"]').click()

    time.sleep(random.randint(1, 5))

    # click year
    se_player.find_element_by_xpath('//*[@id="sp_hitting_season"]/option[2]').click()

    time.sleep(random.randint(1, 5))

    # click player ID
    se_player.find_element_by_xpath('//*[@id="sp_hitting_team_id"]').click()

    time.sleep(random.randint(1, 5))

    # pick new york yankees
    se_player.find_element_by_xpath('//*[@id="sp_hitting_team_id"]/option[20]').click()

    time.sleep(random.randint(1, 5))

    # click hitting splits
    se_player.find_element_by_xpath('//*[@id="sp_hitting_hitting_splits"]').click()

    time.sleep(random.randint(1, 5))

    # reset to select-split
    se_player.find_element_by_xpath('//*[@id="sp_hitting_hitting_splits"]/option').click()

    time.sleep(random.randint(10, 15))

    soup_ny_yankees = BeautifulSoup(driver.page_source, 'html.parser')

    s_ny = []

    for tr in soup_ny_yankees.find_all('table')[0].find('tbody'):
        s_ny.append({'player': tr.find('a').get_text(),
                     'position': tr.find('td', {'index': 5}).get_text(),
                     'ab': tr.find('td', {'index': 7}).get_text(),
                     'avg': tr.find('td', {'index': 18}).get_text()})

    write_to_csv('3a', ['player', 'position', 'ab', 'avg'], s_ny)

    # Answer 3a
    val = sorted(s_ny, key=lambda x: int(x['ab']) > 30)[0]
    print(val['player'] + ' ' + val['position'])

    # Answer 3b
    write_to_csv('3b', ['player', 'position', 'ab', 'avg'], s_ny)
    val_b = \
        sorted([s for s in s_ny if s['position'] in ['RF', 'CF', 'LF'] and s['avg'] != '.---'], key=lambda x: x['avg'])[
            -1]
    print(val_b['player'] + ' ' + val_b['position'])

    # 4
    # // *[ @ id = "sp_hitting_season"]

    # click year drop down
    se_player.find_element_by_xpath('// *[ @ id = "sp_hitting_season"]').click()

    time.sleep(random.randint(1, 5))

    # go to 2015
    se_player.find_element_by_xpath('//*[@id="sp_hitting_season"]/option[4]').click()

    time.sleep(random.randint(1, 5))

    # click AL
    se_player.find_element_by_xpath('//*[@id="sp_hitting-1"]/fieldset[1]/label[2]/span').click()

    time.sleep(random.randint(1, 5))

    # click teams drop-down
    se_player.find_element_by_xpath('//*[@id="sp_hitting_team_id"]').click()

    time.sleep(random.randint(1, 5))

    # reset path to all
    se_player.find_element_by_xpath('//*[@id="sp_hitting_team_id"]/option[1]').click()

    time.sleep(random.randint(1, 5))

    soup_top_al = BeautifulSoup(driver.page_source, 'html.parser')

    t_al = []

    for tr in soup_top_al.find_all('table')[0].find('tbody'):
        t_al.append({'player': tr.find('a').get_text(),
                     'position': tr.find('td', {'index': 5}).get_text(),
                     'ab': tr.find('td', {'index': 7}).get_text()})

    write_to_csv('4', ['player', 'position', 'ab'], t_al)

    ans_4 = sorted(t_al, key=lambda x: int(x['ab']))[-1]

    print('Answer 4')
    print(ans_4['player'] + ' ' + ans_4['ab'] + ' ' + ans_4['position'])

    driver.quit()


most_home_runs()


    #Answers 6

import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '470fa0ee7e7a40fab4394282a0fe799d',
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('api.fantasydata.net')
    conn.request("GET", "/v3/mlb/stats/json/Games/2016?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))