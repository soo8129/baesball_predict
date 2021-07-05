# 네이버 스포츠 경기결과 참조해서 라인업순 타율과 해당 선수 변수 넣음
# input game_id, home_away, player_id
# output [1, ..., 8, player_ba, player_hit_num, is_hit]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://m.sports.naver.com/game/'


def get_player_id(href=None):
    player_id_loc = href.find('playerId=') + 9
    player_id = href[player_id_loc:player_id_loc + 5]
    return player_id


def get_lineup_vars(game_id='20210624NCLT02021', home_away='원정경기', player_id='76232'):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)
    URL_RECORD = URL + game_id + '/record'
    driver.get(URL_RECORD)
    driver.implicitly_wait(3)

    if home_away == '원정경기':
        driver.find_element_by_xpath('//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]/div[1]/div/button[1]') \
            .click()
        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]'
                                                          '/div[2]/div[1]/div[1]'))
            )
        except EC as e:
            print(e)

    player_name = driver.find_elements_by_xpath('//*[@id="content"]/div/div/section[2]'
                                                '/div[2]/div/div[6]/div[2]/div[1]/div[1]/ul')
    player_record = driver.find_elements_by_xpath('//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]/div[2]'
                                                  '/div[1]/div[2]/div/div/table/tbody')
    try:
        name_column = player_name[0].find_elements_by_tag_name('a')
    except Exception as e:
        print(e, player_id, home_away, game_id, 'no tag')
    lineup_player_id = []
    for name in name_column:
        name_href = name.get_attribute('href')
        lineup_player_id.append(get_player_id(name_href))

    lineup_vars = []
    tmp_ba = ''
    hit_num = ''
    is_hit = '0'
    pre_order = '0'
    player_record_trs = player_record[0].find_elements_by_tag_name('tr')
    for i in range(len(lineup_player_id)):
        bat_order = player_record_trs[i].find_element_by_tag_name('a').text
        tds = player_record_trs[i].find_elements_by_tag_name('td')
        if bat_order != '교체':
            if lineup_player_id[i] == player_id:
                tmp_ba = tds[7].text
                hit_num = bat_order
                if int(tds[2].text) > 0:
                    is_hit = '1'
            else:
                lineup_vars.append(tds[7].text)
            pre_order = bat_order
        else:
            if lineup_player_id[i] == player_id:
                tmp_ba = tds[7].text
                hit_num = pre_order
                if int(tds[2].text) > 0:
                    is_hit = '1'
                lineup_vars.pop()

    driver.close()

    if len(lineup_vars) != 8:
        print(lineup_vars)
        print(lineup_player_id)
        print(game_id, home_away, player_id, 'something wrong')
    else:
        return lineup_vars + [tmp_ba, hit_num, is_hit]


#print(get_lineup_vars('20210629SSSK02021', '홈경기', '66917'))

