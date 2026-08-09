import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initilizations
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
DATA_FILE = "shared_text.txt"
ENCODING = "utf-8"


def read_saved_text() -> str:
    """
    Returns the currently displayed text
    if not text is found, prompts the user to enter a text
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding=ENCODING) as f:
            return f.read()
    return "Enter your Text here!"


def save_text_to_file(text):
    """Saves new text into the DATA_FILE"""
    with open(DATA_FILE, "w", encoding=ENCODING) as f:
        f.write(text)


@app.route('/')
def home():
    text_content = read_saved_text()
    return render_template('index.html', current_text=text_content)


# Listen for a WebSocket event named 'update_text'
@socketio.on('update_text')
def handle_update_text(data):
    new_text = data.get('content', '')
    save_text_to_file(new_text)
    # 'broadcast=True' sends the new text to EVERY connected client/phone
    emit('text_updated', {'content': new_text}, broadcast=True)


if __name__ == '__main__':
    # Use socketio.run instead of app.run
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
