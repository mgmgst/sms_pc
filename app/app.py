import requests
import config
from flask import Flask,jsonify,redirect,request,render_template

app = Flask(__name__)

@app.route("/message_Send")
def message_Send():
    '''this is test subject for message_Send'''
    return 'message_Send' , 200

@app.route("/get_sms")
def get_sms(): 
    '''this function get and show sms'''
    print("[+] we are getting sms . . . :)")
    data = {"message":"procecd"}
    return jsonify(data) , 200

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

def sendsms(phone,mess):
    url = config.url
    data = {'receptor':phone, 'message':mess}
    respon = requests.post(url,data=data)
    return respon
if __name__ == "__main__":
    app.run("0.0.0.0",5000,debug=True)