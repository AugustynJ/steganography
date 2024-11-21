from flask import Flask, request, render_template, redirect, url_for, request
import os

import TTL.listener
import TTL.sender

app = Flask(__name__)
template_dir = os.path.relpath('./templates')

@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/method_1')
def method_1():
    return render_template('method_1.html')

@app.route('/method_1/client', methods=['GET', 'POST'])
def method_1_client():
    response = ""
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        ip = request.form['ip']
        try:
            if message != "" and ip != "":
                TTL.sender.send_message(message, ip)
                response = "Wiadomość została wysłana!"
        
        except Exception as e:
            response = f"Error: {e}"
    
    return render_template('method_1/client.html', response=response)

@app.route('/method_1/server', methods=['GET', 'POST'])
def method_1_server():
    iface = "lo"
    response = ""
    if request.method == 'POST':
        if iface in request.form:
            iface = request.form['iface']

    try:
        response = TTL.listener.handle_packets(iface, 2000)
        
    except Exception as e:
        response = f"Error: {e}"

    return render_template('method_1/server.html', iface=iface, response=response)



def start_app():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    start_app()