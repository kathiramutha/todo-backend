from flask import Flask, request, jsonify
import pymysql
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    return "Backend running"

@app.route("/tasks", methods=["GET"])
def get_tasks():

    connection=get_connection()

    with connection.cursor() as cursor:

        cursor.execute("SELECT * FROM todos")
        tasks=cursor.fetchall()

    connection.close()

    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])

def add_task():

    data=request.get_json()

    task=data.get("task")

    connection=get_connection()

    with connection.cursor() as cursor:

        cursor.execute("INSERT INTO todos (task) VALUES (%s)",(task))

    connection.commit()
    connection.close()

    return jsonify({"message":"task added"})

if __name__=="__main__":
    app.run()