# -*- coding:utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
from Student.Student import student
from Student.sqlconfig import selectgrade, selectuser
from threading import Thread


app = Flask(__name__)
app.config['SECRET_KEY']='yulupingjyn220ioj3jn'
mannger = Manager(app)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('学号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, "密码在6-15位")])
    submit = SubmitField('查询')

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        passwd = form.password.data
        students = student(name,passwd)
        thr = Thread(target=students.getgrade)
        thr.start()
        # students.getgrade()
        # print(students.info)
        if selectuser(name):
            session['name'] = name
            return redirect(url_for('user', id=name))
        else:
            flash('输入有误')
    if session.get('name') is not None:
        return redirect(url_for('user', id=session.get('name')))

    return render_template('index.html', form=form)

@app.route('/user/<id>')
def user(id):
    if session.get('name') is None:
        return redirect(url_for('index'))
    uid=session.get('name')
    info = selectgrade(uid)
    return render_template('user.html', info=info)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')


if __name__ == '__main__':
    mannger.run()