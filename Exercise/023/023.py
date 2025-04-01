# coding: utf_8
# 使用 Python 的 Web 框架，做一个 Web 版本留言簿应用

import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = "hard to guess string"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config['SQLALCHEMY_COMMIT_ON_TEAEDOWN'] = Ture
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = "user"
	id = db.column(db.Integer, primary_key=True)
	username = db.Column(db.String(64))
	message = db.Column(db.String(64))
	def __repr__(self):
		return "<User {}".format(self.username)

class NameForm(Form):
	name = StringField("What is your name?", validators=[Required()])
	message = TextAreaField("Please leave a message", validators=[Required()])
	submit = SubmitField("Submit")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(505)
def internal_server_error(e):
	return render_template("505.html"), 505

@app.route("/", methods=["GET", "POST"])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User(username=form.name.data, message=form.message.data)
		db.session.add(user)
		return redirect(url_for("index"))
	array = User.query.all()
	if not array:
		flash("这里没有消息，留言吧")
	return render_template("index.html", form=form, array=array)

if __name__ == "__main__":
	db.create_all()
	manager.run()

# 不能用(⊙o⊙)…