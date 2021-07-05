# 2021.07.03 modified
# predict_prob 테이블에서 player_probs 테이블로 데이터 이전
import pymysql
import datetime


def _get_predict_prob():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "SELECT predict_prob.player_id, players.player_name, players.team_name, predict_prob.prob " \
          "FROM predict_prob, players " \
          "WHERE predict_prob.player_id=players.player_id AND date=%s " \
          "ORDER BY prob asc;"
    iso_today = datetime.date.today().isoformat()
    cursor.execute(sql, '2021-07-03')
    rows = cursor.fetchall()
    predict_prob = []
    for row in rows:
        predict_prob.append([row[0], row[1], row[2], row[3]])
    conn.close()

    return predict_prob


# DELETE ALL predict_prob records
def _initialize_probs():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "DELETE FROM player_probs;"
    cursor.execute(sql)
    conn.commit()
    conn.close()


# predict_prob[player_id, player_name, team_name, prob]
def _put_player_probs(predict_prob=None):
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='chldlstns1!',
                           db='baseball',
                           charset='utf8')
    cursor = conn.cursor()
    sql = "INSERT INTO player_probs" \
          "(player_id, player_name, team_name, probability, published_at, created_at, updated_at) " \
          "VALUES(%s, %s, %s, %s, %s, %s, %s);"
    cur_time = datetime.datetime.now().isoformat()
    try:
        for prob in predict_prob:
            cursor.execute(sql, (prob[0], prob[1], prob[2], prob[3], cur_time, cur_time, cur_time))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


def main():
    predict_prob = _get_predict_prob()
    # delete all records from predict_probs
    if predict_prob:
        _initialize_probs()
        _put_player_probs(predict_prob)
    else:
        print(datetime.date.today(), "no prob")


if __name__ == '__main__':
    main()
