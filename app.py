from flask import Flask , jsonify
app = Flask(__name__)

@app.route("/get_sms")
def get_sms(): 
    '''this function get and show sms'''
    print("[+] we are getting sms . . . :)");
    data = {"message":"procecd"}
    return jsonify(data) , 200

@app.route("/send_sms")
def send_sms(): 
    '''this function send sms'''
    pass

if __name__ == "__main__":
    app.run("0.0.0.0",5000,debug=True)