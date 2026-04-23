import os
import socket
import platform
import psycopg2
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)
APP_VERSION = "1.0"

def get_db_connection():
    """Establishes connection using environment variables from Docker Compose."""
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return conn

@app.route('/')
def greeting():
    hostname = socket.gethostname()
    return f"Hello! This request is being served by host: {hostname}\n"

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    })

@app.route('/info')
def info():
    return jsonify({
        "python_version": platform.python_version(),
        "hostname": socket.gethostname(),
        "current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "os_platform": platform.system()
    })

@app.route('/db')
def db_test():
    """Tests the connection to the PostgreSQL container."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({
            "database_status": "connected",
            "database_version": db_version[0]
        })
    except Exception as e:
        return jsonify({
            "database_status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 is necessary to allow docker to run.
    app.run(host='0.0.0.0', port=5000)
