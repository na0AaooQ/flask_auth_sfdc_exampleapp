from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.services import zipcode_service

zipcode = Blueprint('zipcode', __name__)


@zipcode.route('/')
@login_required  # ログインしていないと表示できないようにする
def find_all():
    zipcode = zipcode_service.find_all()
    return render_template('zipcode/index.html', zipcode=zipcode)
