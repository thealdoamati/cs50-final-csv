from flask import Flask, render_template, request, session, redirect
from helpers import check_csv, create_mockup
import pandas as pd
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")     
        action = request.form.get("action")

        if not check_csv(file) or not action:
            return redirect("upload.html")
        
        # Saving file to folder
        saved_path = UPLOAD_FOLDER / file.filename
        file.save(saved_path)
        
        df = pd.read_csv(saved_path)
        new_examples = create_mockup(df)
        
        # Store it in session
        session["file_path"] = str(saved_path)
        session["action"] = action
             
        return render_template("upload.html", new_examples=new_examples, action=action)
    else:  
        return render_template("upload.html")
    
@app.route("/process", methods=["GET", "POST"])
def process():
    if request.method == "POST":
        file_path = session["file_path"] 
        action = session["action"]
        df = pd.read_csv(file_path)
        header = list(df)
        examples = create_mockup(df)
        
        new_header = ", ".join(header)
        
        examples_rows = []
        for each_row in examples:
            new_row = ", ".join(each_row)
            examples_rows.append(new_row)
        new_examples = "\n".join(examples_rows)
        
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_dir_path = Path(tmpdirname)
            
            input_folder = temp_dir_path / "input_csv"
            output_folder = temp_dir_path / "output_files"
            
            input_folder.mkdir()
            output_folder.mkdir()
            
            csv_destination = input_folder / "csv_file.csv"
            shutil.copy(file_path, csv_destination)
             
        return render_template("process.html")
    else:  
        return render_template("process.html")
    