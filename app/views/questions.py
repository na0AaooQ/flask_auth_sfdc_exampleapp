from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.services import question_service

questions = Blueprint('questions', __name__)


@questions.route('/')
@login_required  # ログインしていないと表示できないようにする
def find_all():
    questions = question_service.find_all()
    return render_template('questions/index.html', questions=questions)


@questions.route('/<question_id>')
@login_required  # ログインしていないと表示できないようにする
def find_one(question_id: int):
    question = question_service.find_one(question_id)
    return render_template('questions/show.html', question=question)

#####
@questions.route('/search')
@login_required  # ログインしていないと表示できないようにする
def find_sfdc_data():
    question = question_service.find_sfdc_data()
    print(question)
    return render_template('questions/sfdc_search_show.html', question=question)

@questions.route('/sfdc/search/<question_id>', methods=['GET'])
@login_required  # ログインしていないと表示できないようにする
def find_sfdc_data_id(question_id: int):
    question = question_service.find_sfdc_data_id(question_id)
    flash('Salesforce取引先データを検索しました。')
    return render_template('questions/sfdc_search_show.html', question=question)

@questions.route('/sfdc/search', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def find_sfdc_search_data():
    try:
        if request.method == 'GET':
            return render_template('questions/sfdc_search_post.html')
        else:
            # postとputを一つのメソッドでできるようにquestion_idを入れてあるが、
            # 新規作成時はNoneにしておく。二つ目のrequet.formはformから送られてくる情報をそのままserviceに渡す
            # current_userはflask_loginの機能で、現在ログインしているユーザーの情報を取得することができる。
            print(request.form)
            question = question_service.find_sfdc_search_data(request.form.get('id'))
            flash('Salesforce取引先データを検索しました。')
            return render_template('questions/sfdc_search_post_show_result.html', question=question)
    except Exception:
        flash('Salesforce取引先データを検索できませんでした。')
        return redirect(url_for('questions.sfdc/search'))

#########################################
@questions.route('/sfdc/update', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def update_sfdc_data():
    try:
        if request.method == 'GET':
            return render_template('questions/sfdc_update_post.html')
        else:
            question = question_service.sfdc_data_update(request.form.get('id'), request.form.get('name'))
            flash('Salesforce取引先データを更新しました。')
            return render_template('questions/sfdc_update_show_result.html', question=question)
    except Exception:
        flash('Salesforce取引先データを更新することができませんでした。')
        return redirect(url_for('questions.sfdc/update'))

################################################################################################
@questions.route('/sfdc/create', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def create_sfdc_data():
    try:
        if request.method == 'GET':
            return render_template('questions/sfdc_create_post.html')
        else:
            question = question_service.sfdc_data_create(request.form.get('name'), request.form.get('phone'))
            flash('Salesforce取引先データを登録しました。')
            return render_template('questions/sfdc_create_show_result.html', question=question)
    except Exception:
        flash('Salesforce取引先データを作成することができませんでした。')
        return redirect(url_for('questions.sfdc/create'))

################################################################################################
@questions.route('/sfdc/delete', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def delete_sfdc_data():
    try:
        if request.method == 'GET':
            return render_template('questions/sfdc_delete_post.html')
        else:
            question = question_service.sfdc_data_delete(request.form.get('id'))
            flash('Salesforce取引先データを削除しました。')
            return render_template('questions/sfdc_delete_show_result.html', question=question)
    except Exception:
        flash('Salesforce取引先データを削除することができませんでした。')
        return redirect(url_for('questions.sfdc/delete'))

################################################################################################
@questions.route('/add', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def add():
    try:
        if request.method == 'GET':
            return render_template('questions/post.html')
        else:
            # postとputを一つのメソッドでできるようにquestion_idを入れてあるが、
            # 新規作成時はNoneにしておく。二つ目のrequet.formはformから送られてくる情報をそのままserviceに渡す
            # current_userはflask_loginの機能で、現在ログインしているユーザーの情報を取得することができる。
            question = question_service.save(None, current_user.id, request.form)
            if question is None:
                flash('メモを追加することができませんでした。')
                return redirect(url_for('questions.add'))
            flash('メモを追加しました。')
            return redirect(url_for('questions.find_all'))
    except Exception:
        flash('メモを追加することができませんでした。')
        return redirect(url_for('questions.add'))

@questions.route('/update/<question_id>', methods=['GET', 'POST'])
@login_required  # ログインしていないと表示できないようにする
def update(question_id: int):
    try:
        if request.method == 'GET':
            question = question_service.find_one(question_id)
            return render_template('questions/update.html', question=question)
        else:
            question = question_service.save(question_id, current_user.id, request.form)
            if question is None:
                flash('メモを修正することができませんでした。')
                return redirect(url_for('questions.update', question_id=question_id))
            flash('メモを修正しました。')
            return redirect(url_for('questions.find_all'))
    except Exception:
        flash('メモを修正することができませんでした。')
        return redirect(url_for('questions.update', question_id=question_id))

@questions.route('/delete/<question_id>', methods=['POST'])
@login_required  # ログインしていないと表示できないようにする
def delete(question_id: int):
    try:
        question_service.delete(question_id)
        flash('メモを削除しました。')
        return redirect(url_for('questions.find_all'))
    except Exception:
        flash('メモを削除することができませんでした。')
        return redirect(url_for('questions.find_all'))
