# 2021.07.04 modified
# 네이버 스포츠의 어제 경기결과 참고
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lineup_variables import get_player_id
import pymysql

URL = 'http://m.sports.naver.com/game/'


def _db_players_ba(players_info=None):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "UPDATE players SET ba=%s WHERE player_id=%s;"

    for player_info in players_info:
        cursor.execute(sql, (player_info[1], player_info[0]))
    conn.commit()
    conn.close()


def _pof_id(game_id='20210624NCLT02021', home_away='home'):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    path = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL_RECORD = URL + game_id + '/record'
    driver.get(URL_RECORD)
    driver.implicitly_wait(3)

    if home_away == 'away':
        driver.find_element_by_xpath('//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]/div[1]/div/button[1]') \
            .click()
        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]'
                                                          '/div[2]/div[1]/div[1]/ul'))
            )
        except EC as e:
            print(e, game_id, home_away)

    player_name = driver.find_elements_by_xpath('//*[@id="content"]/div/div/section[2]'
                                                '/div[2]/div/div[6]/div[2]/div[1]/div[1]/ul')
    player_record = driver.find_elements_by_xpath('//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]/div[2]'
                                                  '/div[1]/div[2]/div/div/table/tbody')
    try:
        name_column = player_name[0].find_elements_by_tag_name('a')
    except:
        print('name_column error', game_id, home_away)
        driver.close()
        return []

    lineup_player_id = []
    for name in name_column:
        name_href = name.get_attribute('href')
        lineup_player_id.append(get_player_id(name_href))
    print(lineup_player_id)

    lineup_vars = []
    player_record_trs = player_record[0].find_elements_by_tag_name('tr')
    for i in range(len(lineup_player_id)):
        tds = player_record_trs[i].find_elements_by_tag_name('td')
        # tds[2].text 타수, tds[7].text 타율
        lineup_vars.append([lineup_player_id[i], tds[7].text])

    driver.close()

    return lineup_vars


def info(game_id='20210624NCLT02021'):
    pof_list = _pof_id(game_id, 'home') + _pof_id(game_id, 'away')
    _db_players_ba(pof_list)
    return pof_list


