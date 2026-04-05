from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY, name TEXT NOT NULL)''')
    conn.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice')")
    conn.execute("INSERT OR IGNORE INTO users (id, name) VALUES (2, 'Bob')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "DevSecOps Lab API", "status": "running"})

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    # Parameterized query - prevents SQL injection
    conn = get_db()
    result = conn.execute(
        "SELECT * FROM users WHERE name = ?", (query,)
    )
    users = [dict(row) for row in result.fetchall()]
    conn.close()
    
    return jsonify({"results": users})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    init_db()
    # Use 127.0.0.1 instead of 0.0.0.0 to avoid exposing server publicly
    app.run(host='127.0.0.1', port=8080, debug=False)