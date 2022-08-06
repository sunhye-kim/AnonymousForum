import os
import sys
import pymysql

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import db_conn

def select_forum_list():
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * FROM forum_main;"

    cursor.execute(query)
    forum_data = cursor.fetchall()


def insert_forum_detail(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql_query = """ 
        INSERT INTO `forum_main` 
            (`title`, `content`, `user_name`, `passwd_md5`, `reg_dtime`, `modify_dtime`)
        VALUES (%s, %s, %s, %s, %s, %s);"""
    
    cursor.execute(sql_query, query_args)

