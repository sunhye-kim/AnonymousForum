import os
import sys

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


@forum_api.route('/forumlist', methods=['GET'])
def forumlist():

    if request.method != 'GET':
        return jsonify(
            ErrorHandler.error_405()
        )
    
    try:
        offset_cnt = request.args['offset_cnt']
        limit_cnt = request.args['limit_cnt']
    except:
        return jsonify(
            ErrorHandler.error_400()
        )

    
    title = request.args.get('title', default=None)
    write_user = request.args.get('write_user', default=None)
 
    select_forum_data_args = (offset_cnt, limit_cnt, title, write_user, )
    forum_data = call_query.select_forum_list(select_forum_data_args)

    
    return jsonify(
        SuccessHandler.success_200(forum_data)
    )


@forum_api.route('/detail', methods=['GET', 'POST'])
def forum_detail():
    if request.method == 'GET':
        return jsonify(ErrorHandler.error_405())
    
    elif request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            user_name = request.form['user_name']
            passwd_md5 = request.form['passwd_md5']
            reg_dtime = request.form['reg_dtime']
            modify_dtime = request.form['modify_dtime']

        except:
            return jsonify(ErrorHandler.error_400())

        insert_forum_detail_args = (title, content, user_name, passwd_md5, reg_dtime, modify_dtime, )
        call_query.insert_forum_detail(insert_forum_detail_args)

        return jsonify(
            SuccessHandler.success_201()
        )
    
    # try:
    #     offset_cnt = request.args['offset_cnt']
    #     limit_cnt = request.args['limit_cnt']
    # except:
    #     return jsonify(ErrorHandler.error_400())

    
    # title = request.args.get('title', default=None)
    # write_user = request.args.get('write_user', default=None)
 
    # select_forum_data_args = (offset_cnt, limit_cnt, title, write_user, )
    # forum_data = call_query.select_forum_data(select_forum_data_args)

    
    # return jsonify(
    #     SuccessHandler.success_200(forum_data)
    # )

