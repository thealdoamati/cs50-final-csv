from flask import Flask, render_template, request
import os
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")

        if not file:
            return render_template("index.html")
        
        _, extension = os.path.splitext(file.filename)

        if extension != ".csv":
            print("Only csv")
            return render_template("index.html")
        
        reader = csv.reader(file.stream.read().decode("utf-8").splitlines())
        rows = []
        for row in reader:
            rows.append(row)

        header = rows[0]
        
        print(f"file: {file}")
        return render_template("upload.html")
    else:  
        return render_template("upload.html")
    