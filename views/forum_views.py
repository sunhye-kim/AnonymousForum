import os
import sys
import datetime
import traceback

from flask import Blueprint
from flask import request, jsonify

from . import error_handler
from . import success_handler

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from model import call_query


ErrorHandler = error_handler.ErrorHandler()
SuccessHandler = success_handler.SuccessHandler()

forum_app = Blueprint('forum', __name__, url_prefix='/forum')

@forum_app.route('/')
def test():
    return 'Hello Forum'

class CheckDataType:
    def check_integer(self, param):
        if isinstance(param, int):
            return True
        else:
            return False
    
    def check_string(self, param):
        if isinstance(param, str):
            return True
        else:
            return False
    
    def check_datetime(self, param):
        if isinstance(param, datetime):
            return True
        else:
            return False

####################
# 게시판 리스트
####################
@forum_app.route('/board', methods=['GET'])
def board():
    if request.method == 'GET':
        try:
            offset_cnt = request.args['offset_cnt']
            limit_cnt = request.args['limit_cnt']
        except:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )
        
        title = request.args.get('title', default=None, type=str)
        write_user = request.args.get('write_user', default=None, type=str)

        if (CheckDataType().check_integer(offset_cnt) and 
            CheckDataType().check_integer(limit_cnt) and
            CheckDataType().check_string(title) and
            CheckDataType().check_string(write_user)):
            pass
        else:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )


        try:
            select_forum_data_args = (title, write_user, int(offset_cnt), int(limit_cnt), )
            forum_data, is_error = call_query.select_forum_list(select_forum_data_args)

            if is_error:
                raise Exception
        
        except Exception as ex:
            print(traceback.format_exc())
            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_200(forum_data)
            )


####################
# 게시판 상세 데이터
####################
@forum_app.route('/detail', methods=['GET', 'POST', 'PUT', 'DELETE'])
def forum_detail():
    if request.method == 'GET':
        try:
            forum_no = request.args['forum_no']
        except:
            return jsonify(ErrorHandler.error_400())
        
        if CheckDataType().check_integer(forum_no):
            pass
        else:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )
        
        try:
            select_forum_detail_args = (forum_no, )
            return_data, is_error = call_query.select_forum_detail(select_forum_detail_args)

            if is_error:
                raise Exception
        
        except Exception as ex:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_200(return_data)
            )
    
    elif request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            user_name = request.form['user_name']
            passwd_md5 = request.form['passwd_md5']

        except:
            return jsonify(ErrorHandler.error_400())
        
        reg_dtime = request.form.get('reg_dtime', default=datetime.datetime.now())
        modify_dtime = request.form.get('modify_dtime', default=datetime.datetime.now())

        if (CheckDataType().check_string(title) and 
            CheckDataType().check_string(content) and 
            CheckDataType().check_string(user_name) and 
            CheckDataType().check_string(passwd_md5) and
            CheckDataType().check_datetime(reg_dtime) and
            CheckDataType().check_datetime(modify_dtime)):
            pass
        else:
            return jsonify(
                ErrorHandler.error_400()
            )

        try:
            insert_forum_detail_args = (title, content, user_name, passwd_md5, reg_dtime, modify_dtime, )
            is_error = call_query.insert_forum_detail(insert_forum_detail_args)
        
            if is_error:
                raise Exception
        
        except Exception as ex:
            print(traceback.format_exc())
            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_201()
            )
    
    elif request.method == 'PUT':
        try:
            forum_no = request.form['forum_no']
            user_name = request.form['user_name']
            passwd_md5 = request.form['passwd_md5']

        except:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )
        
        title = request.form.get('title', default=None)
        content = request.form.get('content', default=None)
        modify_dtime = request.form.get('modify_dtime', default=datetime.datetime.now())

        if (CheckDataType().check_integer(forum_no) and 
            CheckDataType().check_string(user_name) and 
            CheckDataType().check_string(passwd_md5) and
            CheckDataType().check_string(title) and
            CheckDataType().check_string(content) and
            CheckDataType().check_datetime(modify_dtime)):
            pass
        else:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )

        try:
            update_forum_detail_args = (title, content, modify_dtime, forum_no, user_name, passwd_md5, )
            is_error = call_query.update_forum_detail(update_forum_detail_args)

            if is_error:
                raise Exception

        except Exception as ex:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_201()
            )

    elif request.method == 'DELETE':
        try:
            forum_no = request.form['forum_no']
            user_name = request.form['user_name']
            passwd_md5 = request.form['passwd_md5']

        except:
            print(traceback.format_exc())
            
            return jsonify(ErrorHandler.error_400())
        
        modify_dtime = request.form.get('modify_dtime', default=datetime.datetime.now())

        if (CheckDataType().check_integer(forum_no) and 
            CheckDataType().check_string(user_name) and 
            CheckDataType().check_string(passwd_md5) and
            CheckDataType().check_datetime(modify_dtime)):
            pass
        else:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )

        try:
            delete_forum_detail_args = (modify_dtime, forum_no, user_name, passwd_md5, )
            is_error = call_query.delete_forum_detail(delete_forum_detail_args)

            if is_error:
                raise Exception
        
        except Exception as ex:
            print(traceback.format_exc())

            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_204()
            )


####################
# 댓글
####################
@forum_app.route('/comment', methods=['GET', 'POST'])
def forum_comment():
    if request.method == 'GET':
        try:
            forum_no = request.args['forum_no']
            offset_cnt = request.args['offset_cnt']
            limit_cnt = request.args['limit_cnt']
        except:
            print(traceback.format_exc())
            
            return jsonify(ErrorHandler.error_400())
        
        if (CheckDataType().check_integer(forum_no) and 
            CheckDataType().check_integer(offset_cnt) and 
            CheckDataType().check_integer(limit_cnt) ):
            pass
        else:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )

        try:
            select_forum_comment_args = (forum_no, int(offset_cnt), int(limit_cnt), )
            return_data, is_error = call_query.select_forum_comment(select_forum_comment_args)

            if is_error:
                raise Exception
        
        except Exception as ex:
            print(traceback.format_exc())

            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_200(return_data)
            )
    
    elif request.method == 'POST':
        try:
            comment_content = request.form['comment_content']
            forum_no = request.form['forum_no']
            user_name = request.form['user_name']

        except:
            return jsonify(ErrorHandler.error_400())

        comment_group = request.form.get('comment_group', default=None)
        reg_dtime = request.form.get('reg_dtime', default=datetime.datetime.now())

        if (CheckDataType().check_string(comment_content) and
            CheckDataType().check_integer(forum_no) and 
            CheckDataType().check_string(user_name) and 
            CheckDataType().check_string(comment_group) and
            CheckDataType().check_datetime(reg_dtime)):
            pass

        else:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )

        if comment_group:
            comment_class = 2
        else:
            comment_class = 1

        try:
            insert_forum_comment_args = (comment_content, forum_no, user_name, comment_class, comment_group, reg_dtime, )
            is_error = call_query.insert_forum_comment(insert_forum_comment_args)

            if is_error:
                raise Exception
        
        except Exception as ex:
            print(traceback.format_exc())

            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_201()
            )


####################
# 키워드 알림 기능
####################
@forum_app.route('/alert', methods=['GET'])
def alert_keyword():
    if request.method == 'GET':
        forum_no = request.form.get('forum_no', default=None)
        comment_no = request.form.get('comment_no', default=None)

        if (CheckDataType().check_integer(forum_no) and
            CheckDataType().check_integer(comment_no) ):
            pass

        else:
            print(traceback.format_exc())
            
            return jsonify(
                ErrorHandler.error_400()
            )

        if forum_no or comment_no:
            pass
            
        else:
            return jsonify(
                ErrorHandler.error_400()
            )
        
        try:
            select_alert_keyword_args = (forum_no, comment_no, )
            return_data, is_error = call_query.select_alert_keyword(select_alert_keyword_args)

            if is_error:
                raise Exception
        
        except Exception as ex:
            print(traceback.format_exc())

            return jsonify(
                ErrorHandler.error_500(ex)
            )

        else:
            return jsonify(
                SuccessHandler.success_200(return_data)
            )

