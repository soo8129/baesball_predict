# 2021.07.04 modified
# 어제 경기 결과 저장
import game_id_to_pass_or_fail_id
import date_to_game_id
import datetime
import save_pof_db


# today date
def _today():
    today = datetime.datetime.now().strftime('%Y-%m-%d').split('-')
    now_year = int(today[0])
    now_month = int(today[1])
    now_date = int(today[2])
    return [now_year, now_month, now_date]


def main():
    today = _today()
    yesterday = [today[0], today[1], today[2] - 1]
    _yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    game_info = date_to_game_id.get_game_id(yesterday[0], yesterday[1], yesterday[2])

    for game in game_info:
        player_pof_list = game_id_to_pass_or_fail_id.info(game[0])
        save_pof_db.save(player_pof_list, game[1], _yesterday, game[0])
    print(today)


if __name__ == '__main__':
     main()

