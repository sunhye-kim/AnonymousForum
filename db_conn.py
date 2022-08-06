import os
import json
import pathlib
import pymysql

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')  # secrets.json 파일 위치를 명시
with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        print(error_msg)

        
DB_CONN =  get_secret("DATABASE")

db_connection = pymysql.connect(
	user    = DB_CONN['USER'],
    passwd  = DB_CONN['PASSWORD'],
    host    = 'localhost',
    db      = 'anonymous_forum',
    charset = 'utf8'
)