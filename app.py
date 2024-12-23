from flask import Flask, request, jsonify
import mysql.connector  

app = Flask(__name__)


def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  
        password='password',  
        database='portfolio'
    )
    return conn

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data['username']
    message = data['message']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (username, message) VALUES (%s, %s)', (username, message))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'status': 'success'}), 200

@app.route('/get_messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM messages ORDER BY timestamp DESC')
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
