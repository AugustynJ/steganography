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



@app.route('/method_2')
def method_2():
    return render_template('method_2.html')

@app.route('/method_2/client', methods=['GET', 'POST'])
def method_2_client():

    return render_template('method_2/client.html')

@app.route('/method_2/server', methods=['GET', 'POST'])
def method_2_server():

    return render_template('method_2/server.html')



@app.route('/method_3')
def method_3():
    return render_template('method_3.html')

@app.route('/method_3/client', methods=['GET', 'POST'])
def method_3_client():

    return render_template('method_3/client.html')

@app.route('/method_3/server', methods=['GET', 'POST'])
def method_3_server():

    return render_template('method_3/server.html')



@app.route('/method_4')
def method_4():
    return render_template('method_4.html')

@app.route('/method_4/client', methods=['GET', 'POST'])
def method_4_client():

    return render_template('method_4/client.html')

@app.route('/method_4/server', methods=['GET', 'POST'])
def method_4_server():

    return render_template('method_4/server.html')



@app.route('/method_5')
def method_5():
    return render_template('method_5.html')

@app.route('/method_5/client', methods=['GET', 'POST'])
def method_5_client():

    return render_template('method_5/client.html')

@app.route('/method_5/server', methods=['GET', 'POST'])
def method_5_server():

    return render_template('method_5/server.html')



@app.route('/method_6')
def method_6():
    return render_template('method_6.html')

@app.route('/method_6/client', methods=['GET', 'POST'])
def method_6_client():

    return render_template('method_6/client.html')

@app.route('/method_6/server', methods=['GET', 'POST'])
def method_6_server():

    return render_template('method_6/server.html')



@app.route('/method_7')
def method_7():
    return render_template('method_7.html')

@app.route('/method_7/client', methods=['GET', 'POST'])
def method_7_client():

    return render_template('method_7/client.html')

@app.route('/method_7/server', methods=['GET', 'POST'])
def method_7_server():

    return render_template('method_7/server.html')




def start_app():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    start_app()