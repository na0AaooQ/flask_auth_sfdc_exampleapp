# モジュールインポート
from flask import Flask, render_template
# データベースを利用するために追加
from flask_sqlalchemy import SQLAlchemy
# flaks-loginのライブラリ追加
## from flask_login import LoginManager
# flaks-loginのライブラリ追加
from flask_login import LoginManager, login_required

# 外部API呼び出し
import requests

##### .env
import os
from os.path import join, dirname
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
##load_dotenv()
#####

# Flaskアプリの生成
app = Flask(__name__)

# ここから /// データベースの設定
app.secret_key = "super secret key"
###app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qa-site.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ここまで /// データベースの設定

# sqlalchemyを通してflaskからdbアクセスをするための入り口
db = SQLAlchemy(app)

# flask-loginに関する設定
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# データベースのimport
from app.models.user import User
from app.models.question import Question

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authに関するルーティングを追加
from app.views.auth import auth
from app.views.zipcode import zipcode
from app.views.questions import questions

# authに関するルートをflaskアプリであるappに追加
app.register_blueprint(auth)
app.register_blueprint(zipcode, url_prefix='/zipcode')
# url_prefixに「/questions」を入れると
# http://localhost:5000/questions/ というリンクになりわかりやすくなるので設定を追加しました
app.register_blueprint(questions, url_prefix='/questions')

# indexのルート設定
@app.route('/')
@login_required  # ここを追加
def index():
    return render_template('index.html')
