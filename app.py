from flask import Flask, request, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/exercise_1')
def exercise_1():
    return "TBD"

def start_app():
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    start_app()