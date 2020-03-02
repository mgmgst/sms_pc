import requests
import config
import MySQLdb
from flask import Flask, flash, jsonify, redirect, request, render_template, url_for, Response, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
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

@app.errorhandler(404)
@login_required
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash
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

@app.route(f"/{config.callbacktoken}/get_sms",methods=["GET", "POST"])
@login_required
def get_sms():
    '''this is getting sms function'''
    # TODO: add graphical page and showing get sms list
    if request.method == 'POST':
        data = request.form
        sender = data["from"]
        message = data["message"]
        writing_sms_to_database(sender,message)
        redirect(url_for('get_sms'))
    
    else:
        # TODO: find way for showing all values not news one and make it more ghrapical
        result = dict(reading_smss_from_database())
        return result, 200
        # maybe we use this type under :
        #ret = {"sender":sender,"message":message}
        #return jsonify(ret) , 200    

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
@limiter.limit("10 per minute")
def login():
    '''this function return login page'''
    message = None
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check(username,password):
            login_user(user)
            flash('ورود به سرور موفق')
            return redirect(url_for('send_sms'))
        else:
            message = 'نام کاربری یا رمز عبور اشتباه می باشد'

    return render_template('login.html', message=message)            

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

# TODO: make database open for ever for adding works from add page to it when i togel it my self close it
def writing_sms_to_database(sender,message):
    
    db=MySQLdb.connect(host=config.MYSQL_HOST,
                       user=config.MYSQL_USER,
                       passwd=config.MYSQL_PASS,
                       db=config.MYSQL_DB)
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS messages;")
    cur.execute("""CREATE TABLE messages (sender VARCHAR(100) , message VARCHAR(250));""")
    db.commit()    
    qury = f'INSERT INTO messages VALUES ("{sender}","{message}");'
    cur.execute(qury)
    db.commit()
    db.close()

def reading_smss_from_database():

    db=MySQLdb.connect(host=config.MYSQL_HOST,
                       user=config.MYSQL_USER,
                       passwd=config.MYSQL_PASS,
                       db=config.MYSQL_DB)
    cur = db.cursor()
    cur.execute("SELECT * FROM messages;")
    db.close()
    return cur.fetchall()


if __name__ == "__main__":
    app.run("0.0.0.0",5000,debug=True)