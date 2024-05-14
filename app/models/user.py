from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

####
# 追加
from sqlalchemy.orm import relationship
####

# モデルに関する設定
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))

    # 追加
    # user.questions と記述することでhas_manyなquestionを取得することができます
    questions = relationship('Question')

    # モデルからインスタンスを生成するときに使います。(利便性を高めるため)
    # passwordの暗号化も自動で行うことができるので、安全性も高めることができます。
    @classmethod
    def from_args(cls, name: str, email: str, password: str):
        instance = cls()
        instance.name = name
        instance.email = email
        if password is not None:
            # passwordがあれば暗号化します。
            instance.hash_password(password)
        return instance

    # 暗号化するためのメソッド。
    def hash_password(self, clean_password):
        self.password = generate_password_hash(str(clean_password), method='pbkdf2:sha256')

    # 登録したpasswordとユーザーがログインフォームで入力したパスワードが正しいかどうかのチェックを行うメソッド
    ## https://pancokeiba.hatenablog.com/entry/2023/10/14/182710
    # 登録したpasswordとユーザーがログインフォームで入力したパスワードが正しいかどうかのチェックを行うメソッド
    def check_password(self, hash_password, clean_password):

        auth_password_chk_flg = check_password_hash(self.password, clean_password)
        print("auth_password_chk_flg")
        print(auth_password_chk_flg)
        return auth_password_chk_flg
