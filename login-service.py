from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)

# Helper function to get database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    identifier = data.get('identifier') # Can be username, email, or mobile
    password = data.get('password')

    if not identifier or not password:
        return jsonify({"error": "Identifier and password are required."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to check if the user exists by username, email, or mobile
    query = """
        SELECT * FROM users
        WHERE username = ? OR email = ? OR mobile = ?
    """
    cursor.execute(query, (identifier, identifier, identifier))
    user = cursor.fetchone()
    conn.close()

    # Verify user existence and password hash
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        # Credentials are correct - Proceed
        return jsonify({
            "message": "Authentication successful.",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email']
            }
        }), 200
    else:
        # Credentials are incorrect - Return error
        return jsonify({"error": "Invalid credentials. Please check your username/email/mobile and password."}), 401

if __name__ == '__main__':
    app.run(debug=False)
