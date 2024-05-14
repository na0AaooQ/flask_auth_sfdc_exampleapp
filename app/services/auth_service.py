##from flask_login import login_user
from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.user import User

# 新規登録を行うためのメソッドです。引数にはviewsで取得するformデータが送られてきます。
def signup(data: {}) -> User:  # -> User：これはreturnする値の型を指定しています。Userはオブジェクトとして出力します。
    try:
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        # ユーザーがすでに登録されているかどうかを確認します
        user = User.query.filter_by(email=email).first()
        if user:
            # 同じメールアドレスでユーザーが登録されているのであればユーザーをリターンします
            return user
        # ユーザーがいなければ作成します
        new_user = User.from_args(name, email, password)
        # データベースに追加するところ
        db.session.add(new_user)
        db.session.commit()
        return user
    except SQLAlchemyError:
        raise SQLAlchemyError

def login(data: {}) -> [User, bool]:

    login_flg = False

    try:
        email = data.get('email')
        password = data.get('password')
        remember = True if data.get('remember') else False
        user = User.query.filter_by(email=email).first()
        # ユーザーとパスワードの確認
        if user and len(email) >= 1 and len(password) >= 1 and email.find('@') >= 1 and user.check_password(user.password, password):
            # ログイン。rememberにチェックを入れていればログインが維持される
            login_user(user, remember=remember)
            login_flg = True
        elif not password:
            login_flg = False
        else:
            login_flg = False

        print("login_flg")
        print(login_flg)
        return user, login_flg

    except SQLAlchemyError:
        raise SQLAlchemyError

def logout():
    logout_user()
    return True
