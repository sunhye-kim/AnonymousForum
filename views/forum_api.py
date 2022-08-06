import os
import sys
import datetime

from email.policy import default
from flask import Blueprint
from flask import request, jsonify

from . import error_handler
from . import success_handler

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from model import call_query


ErrorHandler = error_handler.ErrorHandler()
SuccessHandler = success_handler.SuccessHandler()

forum_api = Blueprint('forum', __name__, url_prefix='/forum')

@forum_api.route('/')
def test():
    return 'Hello Forum'


####################
# 게시판 리스트
####################
@forum_api.route('/board', methods=['GET'])
def board():
    if request.method == 'GET':
        try:
            offset_cnt = request.args['offset_cnt']
            limit_cnt = request.args['limit_cnt']
        except:
            return jsonify(
                ErrorHandler.error_400()
            )

        title = request.args.get('title', default=None)
        write_user = request.args.get('write_user', default=None)
    
        select_forum_data_args = (title, write_user, int(offset_cnt), int(limit_cnt), )
        forum_data = call_query.select_forum_list(select_forum_data_args)
        
        return jsonify(
            SuccessHandler.success_200(forum_data)
        )

    else:
        return jsonify(
            ErrorHandler.error_405()
        )   


####################
# 게시판 상세 데이터
####################
@forum_api.route('/detail', methods=['GET', 'POST', 'PUT', 'DELETE'])
def forum_detail():
    if request.method == 'GET':
        try:
            forum_no = request.args['forum_no']
        except:
            return jsonify(ErrorHandler.error_400())
        
        select_forum_detail_args = (forum_no, )
        return_data = call_query.select_forum_detail(select_forum_detail_args)

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

        insert_forum_detail_args = (title, content, user_name, passwd_md5, reg_dtime, modify_dtime, )
        call_query.insert_forum_detail(insert_forum_detail_args)

        return jsonify(
            SuccessHandler.success_201()
        )
    
    elif request.method == 'PUT':
        try:
            forum_no = request.form['forum_no']
            user_name = request.form['user_name']
            passwd_md5 = request.form['passwd_md5']

        except:
            return jsonify(ErrorHandler.error_400())
        
        title = request.form.get('title', default=None)
        content = request.form.get('content', default=None)
        modify_dtime = request.form.get('modify_dtime', default=datetime.datetime.now())

        update_forum_detail_args = (title, content, modify_dtime, forum_no, user_name, passwd_md5, )
        call_query.update_forum_detail(update_forum_detail_args)

        return jsonify(
            SuccessHandler.success_201()
        )

    elif request.method == 'DELETE':
        try:
            forum_no = request.form['forum_no']
            user_name = request.form['user_name']
            passwd_md5 = request.form['passwd_md5']

        except:
            return jsonify(ErrorHandler.error_400())
        
        modify_dtime = request.form.get('modify_dtime', default=datetime.datetime.now())

        delete_forum_detail_args = (modify_dtime, forum_no, user_name, passwd_md5, )
        call_query.delete_forum_detail(delete_forum_detail_args)

        return jsonify(
            SuccessHandler.success_204()
        )

    else:
        return jsonify(
            ErrorHandler.error_405()
        )

