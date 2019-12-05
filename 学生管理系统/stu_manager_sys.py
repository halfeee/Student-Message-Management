# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import cgi
import codecs
import sys
import sqlite3
import os

app = Flask(__name__)


#登录进入初始界面
@app.route('/',methods=['GET'])
def index():

    return render_template('login.html');


#登录信息处理
@app.route('/login',methods=['POST','GET'])
def login():
    account = "";
    password = "";
    if 'account' not in request.args:
        account = "";
    else:
        account = request.args['account'];
    if 'password' not in request.args:
        password = "1";
    else:
        password = request.args['password'];

#检测是否为管理员
    sql = "select * from managers where id ='"+account+"'and password='"+password+"'";
    database = "database\Stu_Message_manger.db"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()  # 获得查询的结果
    cur.close()
    print(sql)
    print(result.__len__());
    if(result.__len__()!=0):
        return render_template('manager.html',account=result[0][0],name=result[0][1],sex=result[0][2]);
#检测是否为学生
    sql = "select * from student where id ='" + account + "'and password='" + password + "'";
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()  # 获得查询的结果
    cur.close()
    print(sql)
    print(result.__len__());
    if (result.__len__() != 0):
        return render_template('student.html', data=result[0]);
#检测是否为教师
    sql = "select * from teacher where id ='" + account + "'and password='" + password + "'";
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()  # 获得查询的结果
    cur.close()
    print(sql)
    print(result.__len__());
    if (result.__len__() != 0):
        return render_template('teacher.html', data=result[0]);
    return render_template('login.html', message="用户名或密码错误");

@app.route('/manager',methods=['GET'])
def to_change_manager_inf():
    id = request.args['id'];
    name = request.args['name'];
    sex = request.args['sex']
    print(id+" "+name+" "+sex);
    return render_template('manager_chg_information.html',account=id,name=name,sex=sex);


@app.route('/manager_change',methods=['GET'])
def manager_change():
    account = request.args['new_account'];
    name = request.args['new_name'];
    sex = request.args['new_sex'];
    password = request.args['new_password'];
    sql = "update managers set name = '"+name+"' ,sex = '"+sex+"',password = '"+password+"'  where id='"+account+"'"
    database = "database\Stu_Message_manger.db"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(sql);
    conn.commit();
    cur.close();
    print(sql);
    return render_template('login.html');

if __name__ == '__main__':
    app.run(debug=True)
