import os
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initilizations
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
DATA_FILE = "shopping_list.json"
ENCODING = "utf-8"


def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding=ENCODING) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_items(items):
    with open(DATA_FILE, "w", encoding=ENCODING) as f:
        json.dump(items, f, indent=2)


@app.route('/')
def home():
    items = load_items()
    return render_template('index.html', items=items)


@socketio.on('add_item')
def handle_add_item(data):
    item_name = data.get('name', '').strip()
    if item_name:
        items = load_items()
        # Create a unique ID using the highest existing ID + 1
        new_id = max([i['id'] for i in items], default=0) + 1
        new_item = {"id": new_id, "name": item_name, "done": False}
        items.append(new_item)
        save_items(items)
        # Broadcast the new full list to every connected phone
        emit('list_updated', items, broadcast=True)


@socketio.on('toggle_item')
def handle_toggle_item(data):
    item_id = data.get('id')
    items = load_items()
    for item in items:
        if item['id'] == item_id:
            item['done'] = not item['done']
            break
    save_items(items)
    emit('list_updated', items, broadcast=True)


@socketio.on('delete_item')
def handle_delete_item(data):
    item_id = data.get('id')
    items = load_items()
    items = [item for item in items if item['id'] != item_id]
    save_items(items)
    emit('list_updated', items, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
