from flask import Flask, request, render_template, redirect, url_for, request
import os

import TTL.listener
import TTL.sender

import port_number.sender
import port_number.listener

import ports_time.client
import ports_time.server

app = Flask(__name__)
template_dir = os.path.relpath('./templates')

@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html')


# TTL
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


# port number
@app.route('/method_4')
def method_4():
    return render_template('method_4.html')

@app.route('/method_4/client', methods=['GET', 'POST'])
def method_4_client():
    response = ""
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        ip = request.form['ip']
        try:
            if message != "" and ip != "":
                port_number.sender.send_message(message, 4444, ip)
                response = "Wiadomość została wysłana!"
        
        except Exception as e:
            response = f"Error: {e}"
    
    return render_template('method_4/client.html', response=response)

@app.route('/method_4/server', methods=['GET', 'POST'])
def method_4_server():
    ip = "127.0.0.1"
    response = ""
    if request.method == 'POST':
        if ip in request.form:
            ip = request.form['ip']

    try:
        response = port_number.listener.receive_message(4444, ip)
        
    except Exception as e:
        response = f"Error: {e}"

    return render_template('method_4/server.html', ip=ip, response=response)



@app.route('/method_5')
def method_5():
    return render_template('method_5.html')

@app.route('/method_5/client', methods=['GET', 'POST'])
def method_5_client():

    return render_template('method_5/client.html')

@app.route('/method_5/server', methods=['GET', 'POST'])
def method_5_server():

    return render_template('method_5/server.html')


# port + time
@app.route('/method_6')
def method_6():
    return render_template('method_6.html')

@app.route('/method_6/client', methods=['GET', 'POST'])
def method_6_client():
    response = ""
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        ip = request.form['ip']
        try:
            if message != "" and ip != "":
                p_0, factor, delta, MOD, TIMEOUT = ports_time.client.recv_initial_values()
                print(p_0, factor, delta, MOD, TIMEOUT)
                ports_time.client.send_msg_to_server(message.encode(), p_0, factor, delta, MOD, TIMEOUT)
                response = "Wiadomość została wysłana!"
        
        except Exception as e:
            response = f"Error: {e}"
    
    return render_template('method_6/client.html', response=response)

@app.route('/method_6/server', methods=['GET', 'POST'])
def method_6_server():
    ip = "127.0.0.1"
    response = ""
    if request.method == 'POST':
        if ip in request.form:
            ip = request.form['ip']

    try:
        init_values = {"p_0": 42000, "factor": 3, "delta": 1026, "MOD": 65537, "TIMEOUT": 0.1}
        ports_time.server.send_initial_values(init_values)
        response = ports_time.server.reading_msg_from_client(42000)
        
    except Exception as e:
        response = f"Error: {e}"

    return render_template('method_6/server.html', ip=ip, response=response)



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