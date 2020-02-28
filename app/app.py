import requests
import config
from flask import Flask,jsonify,redirect,request,render_template,flash,url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/ok")
def sys_check():
    '''this function tell that falsk server is ok and running!!'''
    ret = {'status':'ok','message':'[+] flask server is running'}
    return jsonify(ret) , 200

@app.route("/message_Send")
def message_Send():
    '''this is test subject for message_Send'''
    return render_template("sendedsms.html")

@app.route("/get_sms",methods=["GET", "POST"])
def get_sms():
    '''this is getting sms function'''
    #Todo:add graphical page and showing get sms list somthing like buttom print
    data = request.form
    sender = data["from"]
    message = data["message"]
    #print(f"i recived {message} from {sender}")
    ret = {"sender":sender,"message":message}
    return jsonify(ret) , 200    

@app.route("/send_sms",methods=["GET", "POST"])
def send_sms(): 
    '''this function send sms'''
    if request.method == 'POST':
        phone = request.form["phone"]
        message = request.form["message"]
        sendsms(phone,message)
        return redirect("message_Send")      

    else:
        return render_template('index.html')    

@app.route("/",methods=["GET", "POST"])
def login():
    '''this function return login page'''
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check(username,password):
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

if __name__ == "__main__":
    app.run("0.0.0.0",5000,debug=True)