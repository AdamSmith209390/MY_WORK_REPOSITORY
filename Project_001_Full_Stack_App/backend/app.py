# app.py - Updated Flask application with integrated database
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random
import sqlite3
import uuid
import os

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database configuration
# Ensure database is created in the backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BACKEND_DIR, 'app_database.db')

def get_db_connection():
    """Create database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def init_database():
    """Initialize database with tables."""
    conn = get_db_connection()
    
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create contacts table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

@app.route('/')
def home():
    """Root endpoint with API information."""
    return jsonify({
        "message": "Full Stack App Backend API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "status": "active",
        "database": "SQLite",
        "endpoints": {
            "users": "/api/users",
            "contacts": "/api/contacts",
            "database_info": "/api/database-info",
            "health": "/api/health",
            "data": "/api/data"
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Full Stack App Backend",
        "version": "1.0.0",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/data')
def get_data():
    """Legacy endpoint - returns sample data."""
    return jsonify({
        "user_id": random.randint(1, 1000),
        "session_id": f"sess_{random.randint(10000, 99999)}",
        "timestamp": datetime.now().isoformat(),
        "random_number": random.randint(1, 100),
        "message": "Sample data from backend!"
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users from the database."""
    try:
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
        conn.close()
        
        users_list = []
        for user in users:
            users_list.append({
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'created_at': user['created_at']
            })
        
        return jsonify({
            "status": "success",
            "users": users_list,
            "total_users": len(users_list),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Database error: {str(e)}"
        }), 500

@app.route('/api/users', methods=['POST'])
def add_user():
    """Add a new user to the database."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        
        if not name or not email:
            return jsonify({
                "status": "error",
                "message": "Name and email are required"
            }), 400
        
        conn = get_db_connection()
        
        # Check if email already exists
        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Failed to add user (email might already exist)"
            }), 500
        
        # Insert new user
        cursor = conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (name, email)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": f"User '{name}' added successfully",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error adding user: {str(e)}"
        }), 400

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contacts from the database."""
    try:
        conn = get_db_connection()
        contacts = conn.execute('SELECT * FROM contacts ORDER BY submitted_at DESC').fetchall()
        conn.close()
        
        contacts_list = []
        for contact in contacts:
            contacts_list.append({
                'contact_id': contact['contact_id'],
                'name': contact['name'],
                'email': contact['email'],
                'message': contact['message'],
                'submitted_at': contact['submitted_at']
            })
        
        return jsonify({
            "status": "success",
            "contacts": contacts_list,
            "total_contacts": len(contacts_list),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Database error: {str(e)}"
        }), 500

@app.route('/api/contacts', methods=['POST'])
def handle_contact():
    """Handle contact form submissions."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided"
            }), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        message = data.get('message', '').strip()
        
        if not all([name, email, message]):
            return jsonify({
                "status": "error",
                "message": "Name, email, and message are all required"
            }), 400
        
        conn = get_db_connection()
        cursor = conn.execute(
            'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
            (name, email, message)
        )
        contact_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": f"Thank you {name}! Your message has been received.",
            "contact_id": contact_id,
            "timestamp": datetime.now().isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error processing contact: {str(e)}"
        }), 400

@app.route('/api/database-info')
def get_database_info():
    """Get comprehensive database information."""
    try:
        conn = get_db_connection()
        
        # Get table information
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = conn.execute(tables_query).fetchall()
        
        tables_info = []
        for table in tables:
            table_name = table['name']
            count_query = f"SELECT COUNT(*) as count FROM {table_name}"
            count_result = conn.execute(count_query).fetchone()
            
            tables_info.append({
                'name': table_name,
                'row_count': count_result['count']
            })
        
        conn.close()
        
        return jsonify({
            "status": "success",
            "database_info": {
                'database_file': DATABASE,
                'file_exists': os.path.exists(DATABASE),
                'tables': tables_info
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Database info error: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": [
            "/api/health",
            "/api/users",
            "/api/contacts", 
            "/api/database-info",
            "/api/data"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Full Stack App Backend")
    print(f"📊 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🗄️  Database: SQLite ({DATABASE})")
    print(f"🌐 Server: http://localhost:5000")
    print(f"📋 API Documentation: http://localhost:5000")
    print("-" * 50)
    
    # Initialize database
    init_database()
    
    # Add some sample data if tables are empty
    conn = get_db_connection()
    user_count = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    
    if user_count == 0:
        print("📝 Adding sample users...")
        sample_users = [
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com'),
            ('Bob Johnson', 'bob@example.com')
        ]
        
        for name, email in sample_users:
            conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        
        conn.commit()
        print(f"✅ Added {len(sample_users)} sample users")
    
    conn.close()
    
    print("💡 Open your HTML file in a browser to test the frontend!")
    app.run(debug=True, host='0.0.0.0', port=5000)