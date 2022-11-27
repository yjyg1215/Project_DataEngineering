from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html'),200

@app.route('/report')
def report():
    
    return render_template("report.html"), 200