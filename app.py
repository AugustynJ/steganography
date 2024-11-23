from flask import Flask, request, render_template, redirect, url_for, request
import os
import subprocess

import TTL.listener
import TTL.sender

import timing.listener
import timing.sender

import port_number.sender
import port_number.listener

import size.sender
import size.receiver

import ports_time.client
import ports_time.server

import dns_covert_channel.server

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
        response = TTL.listener.handle_packets(iface, 1111)
        
    except Exception as e:
        response = f"Error: {e}"

    return render_template('method_1/server.html', iface=iface, response=response)


# timing
@app.route('/method_2')
def method_2():
    return render_template('method_2.html')

@app.route('/method_2/help')
def method_2_help():
    return render_template('method_2/help.html')

@app.route('/method_2/client', methods=['GET', 'POST'])
def method_2_client():
    response = ""
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        ip = request.form['ip']
        try:
            if message != "" and ip != "":
                timing.sender.send_message(ip, message)
                response = "Wiadomość została wysłana!"
        
        except Exception as e:
            response = f"Error: {e}"
    return render_template('method_2/client.html', response=response)


@app.route('/method_2/server', methods=['GET', 'POST'])
def method_2_server():
    iface = "lo"
    ip="127.0.0.1"
    response = ""
    if request.method == 'POST':
        if iface in request.form:
            iface = request.form['iface']

    try:
        response = timing.listener.receive_message(ip, iface)
        
    except Exception as e:
        response = f"Error: {e}"

    return render_template('method_2/server.html', ip=ip, response=response)

# packet size
@app.route('/method_3')
def method_3():
    return render_template('method_3.html')

@app.route('/method_3/client', methods=['GET', 'POST'])
def method_3_client():
    response = ""
    message = ""
    if request.method == 'POST':
        message = request.form['message']
        ip = request.form['ip']
        try:
            if message != "" and ip != "":
                bits = ''.join(format(ord(char), '08b') for char in message)
                with open("size/bits", 'w') as file:
                    file.write(bits)
                
                size.sender.start_client(ip, 3333, "size/bits")
                response = "Wiadomość została wysłana!"
        
        except Exception as e:
            response = f"Error: {e}"
    return render_template('method_3/client.html', response=response)

@app.route('/method_3/server', methods=['GET', 'POST'])
def method_3_server():
    ip = "127.0.0.1"
    response = ""
    if request.method == 'POST':
        if ip in request.form:
            ip = request.form['ip']

    try:
        response = size.receiver.start_server(ip, 3333)
        
    except Exception as e:
        response = f"Error: {e}"

    return render_template('method_3/server.html', ip=ip, response=response)

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


# METODY AUTORSKIE


# port + time
@app.route('/method_5')
def method_5():
    return render_template('method_5.html')

@app.route('/method_5/client', methods=['GET', 'POST'])
def method_5_client():
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
    
    return render_template('method_5/client.html', response=response)

@app.route('/method_5/server', methods=['GET', 'POST'])
def method_5_server():
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

    return render_template('method_5/server.html', ip=ip, response=response)

# DNS AGH flag
@app.route('/method_6')
def method_6():
    return render_template('method_6.html')

@app.route('/method_6/client', methods=['GET', 'POST'])
def method_6_client():
    response = ""
    ip="127.0.0.1"
    script_path = os.path.join(os.path.dirname(__file__), "dns_covert_channel", "client.sh")
    args = [
    script_path,
    "-p", "6666",
    "--server", ip,
    "--client", "127.0.0.1",
    "--domains-file", "dns_covert_channel/domains_mixed.csv",
    "--dns-forwarder", "8.8.8.8",
    "--resolver-file", "dns_covert_channel/resolver.csv",
    "--secret-site", "start.stegano.com",
    "--agh"
]
    if request.method == 'POST':
        ip = request.form['ip']
        try:
            if ip:
                response = "Rozpoczynanie odpytywania serwera o sekretną wiadomość..."
                try:
                    print("Rozpoczynanie odpytywania serwera o sekretną wiadomość...")
                    result = subprocess.run(
                        args,
                        text=True,
                        capture_output=True,
                        check=True 
                    )
                    print(result.stdout)

                except subprocess.CalledProcessError as e:
                    print(f"Command failed with return code {e.returncode}")
                    print(e.output)
                    print(e.stderr)
                response=result.stdout
        except Exception as e:
            response = f"Error: {e}"
    
    return render_template('method_6/client.html', ip=ip, response=response)

@app.route('/method_6/server', methods=['GET', 'POST'])
def method_6_server():
    ip="127.0.0.1"
    iface="lo"
    response = ""
    if request.method == 'POST':
        iface = request.form.get('iface', iface)
        message = request.form.get('message', "")
        
        try:
            if message:
                print("Rozpoczynanie nasłuchiwania serwera DNS.")
                dns_covert_channel.server.prepare_message(message, 6666)
                print("Zakończono nasłuchiwanie")
                response = "Przygotowano wiadomość dla klienta. Rozpoczęto nasłuchiwanie"
            else:
                response = "Nie podano wiadomości."
        except Exception as e:
            response = f"Error: {e}"
    return render_template('method_6/server.html', ip=ip, iface=iface, response=response)

# DNS with a key
@app.route('/method_7')
def method_7():
    return render_template('method_7.html')

@app.route('/method_7/client', methods=['GET', 'POST'])
def method_7_client():
    response = ""
    ip="127.0.0.1"
    script_path = os.path.join(os.path.dirname(__file__), "dns_covert_channel", "client.sh")
    args = [
    script_path,
    "-p", "7777",
    "--server", ip,
    "--client", "127.0.0.1",
    "--domains-file", "dns_covert_channel/domains_mixed.csv",
    "--dns-forwarder", "8.8.8.8",
    "--resolver-file", "dns_covert_channel/resolver.csv",
    "--secret-site", "start.stegano.com",
]
    if request.method == 'POST':
        ip = request.form['ip']
        try:
            if ip:
                response = "Rozpoczynanie odpytywania serwera o sekretną wiadomość..."
                try:
                    print("Rozpoczynanie odpytywania serwera o sekretną wiadomość...")
                    result = subprocess.run(
                        args,
                        text=True,
                        capture_output=True,
                        check=True 
                    )
                    print(result.stdout)

                except subprocess.CalledProcessError as e:
                    print(f"Command failed with return code {e.returncode}")
                    print(e.output)
                    print(e.stderr)
                response=result.stdout
        except Exception as e:
            response = f"Error: {e}"
    
    return render_template('method_7/client.html', ip=ip, response=response)

@app.route('/method_7/server', methods=['GET', 'POST'])
def method_7_server():
    ip="127.0.0.1"
    iface="lo"
    response = ""
    if request.method == 'POST':
        iface = request.form.get('iface', iface)
        message = request.form.get('message', "")
        
        try:
            if message:
                print("Rozpoczynanie nasłuchiwania serwera DNS.")
                dns_covert_channel.server.prepare_message(message, 7777)
                print("Zakończono nasłuchiwanie")
                response = "Przygotowano wiadomość dla klienta. Rozpoczęto nasłuchiwanie"
            else:
                response = "Nie podano wiadomości."
        except Exception as e:
            response = f"Error: {e}"
    return render_template('method_7/server.html', ip=ip, iface=iface, response=response)



def start_app():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    start_app()