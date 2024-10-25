from flask import Flask, request, render_template, redirect, url_for, request
import os

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

@app.route('/method_1/client')
def method_1_client():
    return render_template('method_1/client.html')

@app.route('/method_1/server')
def method_1_server():
    return render_template('method_1/server.html')

def start_app():
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    start_app()