import os
import sys
import pymysql

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import db_conn


def select_forum_list(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """
        SELECT `forum_no`, `title`, `content`, `user_name`, `reg_dtime`, `modify_dtime`
        FROM `forum_main`
        WHERE `title` = IFNULL(%s, `title`)
          AND `user_name` = IFNULL(%s, `user_name`)
          AND `is_delete` = 0
        LIMIT %s, %s;
    """

    forum_list = list()
    try:
        cursor.execute(sql_query, query_args)
        forum_list = cursor.fetchall()

    except Exception as ex:
        msg = "Query Error, Method: select_forum_list , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))

    finally:
        cursor.close()
        conn.close()

        return forum_list, is_error
    

def select_forum_detail(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """ 
        SELECT `forum_no`, `title`, `content`, `user_name`, `reg_dtime`, `modify_dtime`
        FROM `forum_main`
        WHERE `forum_no` = %s
          AND `is_delete` = 0;
    """

    forum_detail = dict()

    try:
        cursor.execute(sql_query, query_args)
        forum_detail = cursor.fetchone()

    except Exception as ex:
        msg = "Query Error, Method: select_forum_detail , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))

    finally:
        cursor.close()
        conn.close()

        return forum_detail, is_error
    
    
def insert_forum_detail(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """ 
        INSERT INTO `forum_main` 
            (`title`, `content`, `user_name`, `passwd_md5`, `reg_dtime`, `modify_dtime`)
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(sql_query, query_args)

    except Exception as ex:
        msg = "Query Error, Method: insert_forum_detail , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))


    finally:
        cursor.close()
        conn.close()
    
    return is_error


def update_forum_detail(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """ 
        UPDATE `forum_main`
        SET `title` = IFNULL(%s, `title`)
           ,`content` = IFNULL(%s, `content`)
           ,`modify_dtime` = %s
        WHERE `forum_no` = %s
          AND `user_name` = %s
          AND `passwd_md5` = %s;
    """

    try:
        cursor.execute(sql_query, query_args)

    except Exception as ex:
        msg = "Query Error, Method: update_forum_detail , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))

    finally:
        cursor.close()
        conn.close()

        return is_error
    

def delete_forum_detail(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """ 
        UPDATE `forum_main`
        SET `is_delete` = 1
           ,`modify_dtime` = %s
        WHERE `forum_no` = %s
          AND `user_name` = %s
          AND `passwd_md5` = %s;
    """

    try:
        cursor.execute(sql_query, query_args)

    except Exception as ex:
        msg = "Query Error, Method: delete_forum_detail , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))

    finally:
        cursor.close()
        conn.close()

        return is_error


def select_forum_comment(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """ 
        SELECT fc1.`comment_no`, fc1.`comment_content`, fc1.`user_name`, fc1.`reg_dtime`,
       CONCAT('[',GROUP_CONCAT(CONCAT('{"user_name":"',fc2.user_name,'", "comment" : "',fc2.comment_content,'"}')),']') as `re_comment`
        FROM `forum_comment` fc1
          LEFT OUTER JOIN `forum_comment` fc2
          ON fc1.forum_no = fc2.forum_no 
          AND fc1.comment_no = fc2.comment_group
        WHERE fc1.`forum_no` = %s
          AND fc1.class = 1
		GROUP BY fc1.comment_no 
        LIMIT %s, %s;
    """

    forum_comment = list()

    try:
        cursor.execute(sql_query, query_args)
        forum_comment = cursor.fetchall()

    except Exception as ex:
        msg = "Query Error, Method: select_forum_comment , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))

    finally:
        cursor.close()
        conn.close()

        return forum_comment, is_error


def insert_forum_comment(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """ 
        INSERT INTO `forum_comment` 
            (`comment_content`, `forum_no`, `user_name`, `class`, `comment_group`, `reg_dtime`)
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(sql_query, query_args)

    except Exception as ex:
        msg = "Query Error, Method: insert_forum_comment , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))

    finally:
        cursor.close()
        conn.close()

        return is_error


def select_alert_keyword(query_args):
    conn = db_conn.g_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    is_error = False

    sql_query = """ 
        SELECT tab.user_name, tab.keyword
        FROM (SELECT fm.content, ka.user_name, ka.keyword
              FROM forum_main fm cross join keyword_alert ka
              WHERE fm.forum_no = %s ) tab
        WHERE tab.content like CONCAT('%%',tab.keyword, '%%')
        UNION
        SELECT tab.user_name, tab.keyword
        FROM (SELECT fc.comment_content, ka.user_name, ka.keyword
              FROM forum_comment fc cross join keyword_alert ka
              WHERE fc.comment_no = %s ) tab
        WHERE tab.comment_content like CONCAT('%%',tab.keyword, '%%');
    """

    alert_user_list = list()

    try:
        cursor.execute(sql_query, query_args)
        alert_user_list = cursor.fetchall()

    except Exception as ex:
        msg = "Query Error, Method: select_alert_keyword , Error Message: %s" % (ex)
        is_error = True
        print(msg)
        print("query args : {}".format(query_args))

    finally:
        cursor.close()
        conn.close()

        return alert_user_list, is_error

