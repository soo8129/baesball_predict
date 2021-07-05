# 네이버 스포츠 경기결과 참조해서 라인업순 타율과 해당 선수 변수 넣음
# input game_id, home_away, player_id
# output [1, ..., 8, player_ba, player_hit_num, is_hit]
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = 'https://m.sports.naver.com/game/'


# lineup vars and is_hit for sql pof table
# not used
def get_lineup(game_id='20210624NCLT02021', home_away='away', player_id=76232):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    path = 'C:/Users/soo81/webcrawling/chromedriver.exe'
    driver = webdriver.Chrome(path, options=options)
    URL_LINEUP = URL + game_id + '/lineup'
    driver.get(URL_LINEUP)
    driver.implicitly_wait(3)

    # lineup[home, away]
    lineup = driver.find_elements_by_class_name('Lineup_lineup_list__1_CNQ')
    if home_away == 'away':
        lineup_li = lineup[0]
    else:
        lineup_li = lineup[1]

    lineup_a = lineup_li.find_elements_by_tag_name('a')[1:]
    # lineup_player_id[first ~ ninth id]
    lineup_player_id = []
    for li in lineup_a:
        player_id_href = li.get_attribute('href')
        loc_player_id = player_id_href.find('playerId=') + 9
        lineup_player_id.append(player_id_href[loc_player_id:loc_player_id + 5])

    driver.close()


def get_player_id(href=None):
    player_id_loc = href.find('playerId=') + 9
    player_id = href[player_id_loc:player_id_loc + 5]
    return player_id


def get_lineup_vars(game_id='20210624NCLT02021', home_away='away', player_id='76232'):
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
#                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]'
#                                                          '/div[2]/div[1]/div[1]'))
                EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div/section[2]'
                                                '/div[2]/div/div[6]/div[2]/div[1]/div[1]/ul'))
            )
        except EC as e:
            print(e)

    player_name = driver.find_elements_by_xpath('//*[@id="content"]/div/div/section[2]'
                                                '/div[2]/div/div[6]/div[2]/div[1]/div[1]/ul')
    player_record = driver.find_elements_by_xpath('//*[@id="content"]/div/div/section[2]/div[2]/div/div[6]/div[2]'
                                                  '/div[1]/div[2]/div/div/table/tbody')
    name_column = player_name[0].find_elements_by_tag_name('a')
    lineup_player_id = []
    for name in name_column:
        name_href = name.get_attribute('href')
        lineup_player_id.append(get_player_id(name_href))

    lineup_vars = []
    tmp_ba = ''
    hit_num = ''
    is_hit = '0'
    player_record_trs = player_record[0].find_elements_by_tag_name('tr')
    for i in range(len(lineup_player_id)):
        bat_order = player_record_trs[i].find_element_by_tag_name('a').text
        tds = player_record_trs[i].find_elements_by_tag_name('td')
        # for check data
        if bat_order != '교체':
            if lineup_player_id[i] == player_id:
                tmp_ba = tds[7].text
                hit_num = bat_order
                if int(tds[2].text) > 0:
                    is_hit = '1'
            else:
                lineup_vars.append(tds[7].text)

    if len(lineup_vars) != 8:
        print(game_id, home_away, player_id, 'something wrong')
    else:
        # is_hit will be not used
        return lineup_vars + [tmp_ba, hit_num, is_hit]


print(get_lineup_vars('20210627LGSS', 'away', '66018'))

