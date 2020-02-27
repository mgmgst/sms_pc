import requests
import config
from flask import Flask , jsonify , redirect , request

app = Flask(__name__)

@app.route("/message_send")
def message_send(): 
    '''this function get and show sms'''
    return " * message_send" , 200		
		
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
        message = request.form["message"]
	    phone = request.form["phone"]
	    sendsms(phone,message)
	    return redirect("message_send")
    else:
        return render_template('index.html')	

def sendsms(phone,mess):
    url = config.url
    data = {'receptor':phone, 'message':mess}
    respon = requests.post(url,data=data)
if __name__ == "__main__":
    app.run("0.0.0.0",5000,debug=True)