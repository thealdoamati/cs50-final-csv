from flask import Flask, render_template, request
import csv
from helpers import check_csv, create_mockup
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")

        if not check_csv(file):
            return render_template("upload.html")

        df = pd.read_csv(file)
        
        new_examples = create_mockup(df)
             
        return render_template("upload.html", new_examples=new_examples)
    else:  
        return render_template("upload.html")
    
@app.route("/converted", methods=["GET", "POST"])
def converted():
    if request.method == "POST":
        file = request.files.get("file")

        if not check_csv(file):
            return render_template("converted.html")

        df = pd.read_csv(file)
        
        new_examples = create_mockup(df)
             
        return render_template("converted.html", new_examples=new_examples)
    else:  
        return render_template("converted.html")
    