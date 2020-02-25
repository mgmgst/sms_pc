import requests
from flask import Flask , jsonify

app = Flask(__name__)

phone = "09155520952"
mess = input("[+] harchi mikhaibego ta brat be shomarat ersal konam : ")

@app.route("/get_sms")
def get_sms(): 
    '''this function get and show sms'''
    print("[+] we are getting sms . . . :)");
    data = {"message":"procecd"}
    return jsonify(data) , 200

@app.route("/send_sms")
def send_sms(): 
    '''this function send sms'''
    sendsms(phone,mess)

def sendsms(phone,mess):
    api_key='44345A386669384A683450384D2B434A656F5176326937594E6866734136754A2B4B565750415A6A6D66633D'
    url = 'https://api.kavenegar.com/v1/%s/sms/send.json' % (api_key)
    data = {'receptor':phone, 'message':mess}
    respon = requests.post(url,data=data)
    print(respon)
    print(respon.json())

if __name__ == "__main__":
    app.run("0.0.0.0",5000,debug=True)