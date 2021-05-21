from flask import Flask,request, redirect,render_template,flash,url_for,send_from_directory
import run,codingtemp,imagetemp
from werkzeug.utils import secure_filename
import webbrowser

import os
app=Flask(__name__,template_folder="template")

app.config["DOCUMENT_UPLOAD"] = "/home/dhruv/test_flask_project/venv/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["PNG","TXT","PPM"]
app.config["DOWNLOAD_FOLDER"]="/home/dhruv/test_flask_project/venv/download"

@app.route("/success")
def success():
    return render_template("success.html")
 
# def fail():
#     return  webbrowser.open_new_tab('http://127.0.0.1:5000/success')

def allowed_document(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/", methods=["GET", "POST"])
def upload_document():

    if request.method == "POST":

        if request.files:
                document = request.files["document"]

                if document.filename == "":
                    print("No filename")
                    return redirect(url_for("http://127.0.0.1:5000/"))

                if allowed_document(document.filename):
                    document.save(os.path.join(app.config["DOCUMENT_UPLOAD"],document.filename))

                    print("File saved")
                    ext = document.filename.rsplit(".", 1)[1]
                    if ext.upper() in {"PPM","PNG"}:
                        run.img_compress("./uploads/"+document.filename)
                    else:    
                        run.compress("./uploads/"+document.filename)
                    doc= document.filename.rsplit(".",1)[0]

                    return send_from_directory(app.config['DOCUMENT_UPLOAD'],doc +".bin", as_attachment=True)
                else:
                    
                    print("That file extension is not allowed")
                    # return fail()
    return render_template("index.html")


    if __name__=="__main__":
        app.run(debug=True)

 