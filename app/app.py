#Flask main Module
from flask import Flask, redirect ,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

db = SQLAlchemy()
app = Flask(__name__)

# MySQL接続用
# db_uri = "mysql+pymysql://root:password@mysql/ここにDB名?charset=utf8"
# app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
# db = SQLAlchemy(app)

# #テーブル接続クラス
# class hoge(db.Model):
#     __tablename__ = ""
#     Id = db.Column(db.Integer,primary_key = True, autoincrement = True, nullable = False)

@app.route("/")
def route():

    return render_template("index.html",title = "ようこそ")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')