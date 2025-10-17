import flask
from flask import request, json, jsonify

import flask_mysqldb
from flask_mysqldb import MySQL

import requests


app = flask.Flask(__name__)
app.config["DEBUG"] = True

app.config["MYSQL_HOST"] = "db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskdocker"

mysql = MySQL(app)

@app.route("/", methods=["GET"])
def index():
    data = requests.get("https://randomuser.me/api")
    return data.json()

@app.route("/insert-host", methods=["POST"])
def insert_host():
    data = requests.get("https://randomuser.me/api").json()
    username = data["results"][0]["name"]["first"]
    
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO users(name) VALUES(%s)""", (username,))
    mysql.connection.commit()
    cur.close()

    return "Olá " + username

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)