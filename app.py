from flask import Flask, render_template, request
import csv
from helpers import check_csv, create_mockup

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        check_csv(file)
        reader = csv.reader(file.stream.read().decode("utf-8").splitlines())
        
        new_examples = create_mockup(reader)
             
        return render_template("upload.html")
    else:  
        return render_template("upload.html")
    