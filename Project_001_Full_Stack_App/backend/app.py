from flask import Flask, jsonify, render_template
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Backend API is running!",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        "user_id": random.randint(1, 1000),
        "session_id": f"sess_{random.randint(10000, 99999)}",
        "timestamp": datetime.now().isoformat(),
        "random_number": random.randint(1, 100),
        "message": "Data from Python backend!"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "My Full Stack App Backend",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    print("Starting Flask backend server...")
    app.run(debug=True, host='0.0.0.0', port=5000)