from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'] 
    )
    return conn

@app.route('/todos', methods=['GET','POST'])
def todos():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id", (data['task'],))
        todo_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'id':todo_id}), 201
    
    cursor.execute("SELECT id, task FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'id': row[0], 'task': row[1]} for row in todos])

@app.route('/')
def health():
    return "OK", 200