from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql


URL = 'http://m.sports.naver.com/game/'


def _db_players_ba(players_info=[['', '']]):


def _pof_id(game_id='20210624NCLT02021'):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    path = '/usr/local/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=path, chrome_options=options)
    URL = URL + game_id + '/record'
    driver.get(URL)
    driver.implicitly_wait(3)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPAth


    return pof_list


def info(game_id='20210624NCLT02021'):
    pof_list = _pof_id(game_id)
    _db_players_ba(pof_list)
    return pof_list


# for test
print(info('20210624NCLT02021'))

