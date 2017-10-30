from flask import Flask, request, render_template

fl = Flask(__name__);

@fl.route ('/', methods = ['GET', 'POST'])
def home():
    return render_template ('home.html');

@fl.route ('/signin', methods = ['GET'])
def signinForm():
    return render_template ('form.html');

@fl.route ('/signin', methods = ['POST'])
def signin():
    userName = request.form['userName'];
    password = request.form['password'];
    #从request对象读取表单
    if userName == 'user' and password == 'pswd':
        return render_template ('signinOK.html', user = userName);
    else:
        return render_template ('form.html', msg = '用户名或密码错误。\n', user = userName);

if __name__ == "__main__" :
    fl.run();
