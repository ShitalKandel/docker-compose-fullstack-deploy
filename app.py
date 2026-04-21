from flask import Flask, jsonify
import socket
import platform
from datetime import datetime

app = Flask(__name__)
APP_VERSION = "1.0"

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
        "current_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    # We bind to 0.0.0.0 so it's accessible outside the container
    app.run(host='0.0.0.0', port=5000)
