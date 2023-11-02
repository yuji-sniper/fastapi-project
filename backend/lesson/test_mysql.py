import pymysql
from decouple import config

# 環境変数から接続情報を取得
db_host = config("DB_HOST", "localhost")
db_user = config("DB_USER", "root")
db_password = config("DB_PASSWORD", "")
db_name = config("DB_NAME", "test")

# MySQLに接続
try:
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 password=db_password,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        # SQLを実行する
        sql = "SHOW TABLES;"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

except pymysql.MySQLError as e:
    print(f"Error connecting to MySQL Platform: {e}")
finally:
    if connection:
        connection.close()
