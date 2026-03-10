from flask import Flask, render_template, request, session, redirect, send_file, after_this_request
from helpers import check_csv, create_mockup
import pandas as pd
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import os
import shutil
import zipfile
from io import BytesIO

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
        
        df = pd.read_csv(saved_path, dtype=str)
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
        
        base_prompt_path = "prompts/base_prompt.txt"
        
        with open(base_prompt_path, "r") as file:
            content = file.read()
            prompt_text = content.format(
                header=new_header,
                examples=new_examples,
                action=action
            )
        
        
        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_dir_path = Path(tmpdirname)
            
            input_folder = temp_dir_path / "input_csv"
            output_folder = temp_dir_path / "output_files"
            prompt_file_path = temp_dir_path / "prompt.txt"
            
            input_folder.mkdir()
            output_folder.mkdir()
            prompt_file_path.write_text(prompt_text)
            
            script_path = temp_dir_path / "script.py"

            script_content = """\
            # PASTE THE GENERATED PYTHON SCRIPT FROM YOUR LLM BELOW THIS LINE.

            # The script must follow the instructions described in prompt.txt.

            if __name__ == "__main__":
                print("Replace this file with your generated script.")
            """

            script_path.write_text(script_content)
            
            csv_destination = input_folder / "csv_file.csv"
            shutil.copy(file_path, csv_destination)
            
            # Creating zip and managing time before deleting temp folder
            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file in temp_dir_path.rglob("*"):
                    zipf.write(file, file.relative_to(temp_dir_path))

            zip_buffer.seek(0)
            
            # Removing original file
            @after_this_request
            def delete_file(response):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print("Error deleting file:", e)
                
                session.pop("file_path", None)
                session.pop("action", None)
                return response         

            return send_file(
                zip_buffer,
                as_attachment=True,
                download_name="project_package.zip",
                mimetype="application/zip"
            )
             
        return render_template("process.html")
    else:  
        return render_template("process.html")
    