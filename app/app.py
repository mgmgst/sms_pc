import requests
import config
from flask import Flask,jsonify,redirect,request,render_template

app = Flask(__name__)

@app.route("/message_Send")
def message_Send():
    '''this is test subject for message_Send'''
    return render_template("sendedsms.html")

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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check(username,password):
            return redirect("send_sms")
        else:
            return redirect("/")    
    else:
        return render_template("login.html")

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