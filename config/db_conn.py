import os
import json
import pathlib
import pymysql

from dbutils.pooled_db import PooledDB

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

try:
    g_pool = PooledDB(
        creator=pymysql, 
        mincached=1, 
        maxconnections=1, 
        blocking=True, 
        host=DB_CONN["HOST"],
        port=DB_CONN["PORT"],
        user=DB_CONN["USER"],
        password=DB_CONN["PASSWORD"], 
        db=DB_CONN["DATABASE_NAME"], 
        charset='utf8mb4', 
        use_unicode=True, 
        autocommit=True, 
        connect_timeout=3, 
        ping=4
    )

except Exception as ex:
    print(ex)
    print("[Emergency Error] DATABASE cannot connect to MySQL")

