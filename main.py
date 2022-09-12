import base64
from flask import Flask, render_template, request, redirect, url_for, Markup
from pymongo import MongoClient, server_api
app = Flask(__name__)
uri = "mongodb+srv://cluster0.ovzlxql.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri, tls=True, tlsCertificateKeyFile='cert.pem', server_api=server_api.ServerApi('1'))
print(client.list_database_names())
db = client.data
print(db.list_collection_names())


@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        doc = {**request.form}
        doc["firstName"] = str(base64.b64encode(doc["firstName"].encode("utf-8"))).replace("b'", "").replace("'", "")
        doc["lastName"] = str(base64.b64encode(doc["lastName"].encode("utf-8"))).replace("b'", "").replace("'", "")
        db.submissions.insert_one(doc)
        return redirect(url_for("done"))
    return render_template("form.html")

@app.route('/done', methods=["GET"])
def done():
    return render_template("done.html")
