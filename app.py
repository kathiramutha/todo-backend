from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")

def get_connection():
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

@app.route('/tasks', methods=['GET'])
def get_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, task FROM todos")

    rows = cursor.fetchall()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "task": row[1]
        })

    conn.close()

    return jsonify(tasks)


@app.route('/tasks', methods=['POST'])
def add_task():

    data = request.get_json()

    task = data["task"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO todos(task) VALUES(%s)", (task,))

    conn.commit()

    conn.close()

    return jsonify({"message":"Task added"})


if __name__ == '__main__':
    app.run()