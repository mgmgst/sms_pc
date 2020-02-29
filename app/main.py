import requests
import config
import sqlite3
from flask import Flask, jsonify, redirect, request, render_template, url_for, Response, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# config
app.config.update(
    SECRET_KEY = config.secret_key
)

limiter = Limiter(
    app,
    key_func=get_remote_address,
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return "%d" % (self.id)


# create some users with ids 1 to 20       
user = User(0)

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')   
    
# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid) 

@app.route("/ok")
def sys_check():
    '''this function tell that falsk server is ok and running!!'''
    ret = {'status':'ok','message':'[+] flask server is running'}
    return jsonify(ret) , 200

@app.route("/message_Send")
@login_required
def message_Send():
    '''this is test subject for message_Send'''
    return render_template("sendedsms.html")

@app.route("/get_sms",methods=["GET", "POST"])
@login_required
def get_sms():
    '''this is getting sms function'''
    #Todo:add graphical page and showing get sms list somthing like buttom print
    data = request.form
    sender = data["from"]
    message = data["message"]
    #print(f"i recived {message} from {sender}")
    #send_sms(sender,'Hi' + message)
    ret = {"sender":sender,"message":message}
    writing_to_database(sender,message)
    return jsonify(ret) , 200    

@app.route("/",methods=["GET", "POST"])
@login_required
def send_sms(): 
    '''this function send sms'''
    if request.method == 'POST':
        phone = request.form["phone"]
        message = request.form["message"]
        sendsms(phone,message)
        return redirect("message_Send")      

    else:
        return render_template('index.html')    

@app.route("/login",methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    '''this function return login page'''
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check(username,password):
            login_user(user)
            return redirect(url_for('send_sms'))
        else:
            error = '.نام کاربری یا رمز عبور اشتباه می باشد'

    return render_template('login.html', error=error)            

def sendsms(phone,mess):
    url = config.url
    data = {'receptor':phone, 'message':mess}
    respon = requests.post(url,data=data)
    return respon

def check(username,password):
    res = False
    usernamein = config.username
    passwordin = config.password
    if username == usernamein and password == passwordin:
        res = True
    return res    

def writing_to_database(sender,message):
    
    conn = sqlite3.connect(config.DFP)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS messages")
    cur.execute("""CREATE TABLE IF NOT EXISTS messages (
        sender TEXT PRIMARY KEY,
        message TEXT);""")
    conn.commit()    
    qury = f'INSERT INTO messages VALUES ("{sender}","{message}");'
    cur.execute(qury)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    writing_to_database("+98 915 552 0952","salam")
    app.run("0.0.0.0",5000,debug=True)