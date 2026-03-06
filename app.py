from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.form.get("file")

        if not file:
            return render_template("index.html")
        
        print(f"file: {file}")
        return render_template("upload.html")
    else:  
        return render_template("upload.html")
    