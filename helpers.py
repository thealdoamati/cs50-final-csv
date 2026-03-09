from flask import render_template
import os

def check_csv(file):
    if not file:
        return render_template("index.html")
        
    _, extension = os.path.splitext(file.filename)

    if extension != ".csv":
        print("Only csv")
        return render_template("index.html")