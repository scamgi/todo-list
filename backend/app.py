# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS
import sys # To handle potential encoding issues

# Basic setup to handle potential stdout encoding issues on some systems
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)
# IMPORTANT: Enable CORS for your Svelte app's origin
# For development, allowing '*' is okay, but for production,
# restrict it to your Svelte app's actual domain.
CORS(app, resources={r"/api/*": {"origins": "*"}}) # Allow all origins for /api/* routes


# In-memory storage (replace with a database in a real application)
todos_store = {}
next_id = 1

# Helper function to find a todo
def find_todo(todo_id):
    return todos_store.get(todo_id)

# --- API Endpoints ---

# GET /api/todos - Fetch all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    # Convert the dictionary values (todos) into a list
    return jsonify(list(todos_store.values()))

# POST /api/todos - Add a new todo
@app.route('/api/todos', methods=['POST'])
def add_todo():
    global next_id
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    text = request.json['text'].strip()
    if not text:
         return jsonify({"error": "'text' cannot be empty"}), 400

    new_todo = {
        "id": next_id,
        "text": text,
        "completed": False
    }
    todos_store[next_id] = new_todo
    next_id += 1
    # Return the created todo with a 201 Created status
    return jsonify(new_todo), 201

# PUT /api/todos/<int:todo_id> - Update a todo (toggle complete)
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    # We'll primarily use PUT to toggle completion status
    # Optionally, you could accept 'text' or 'completed' in the request body
    # for more general updates.
    completed_update = request.json.get('completed')

    if completed_update is not None and isinstance(completed_update, bool):
         todo['completed'] = completed_update
    else:
         # Default behavior: toggle if 'completed' not provided or invalid
         todo['completed'] = not todo['completed']


    todos_store[todo_id] = todo # Update the store
    return jsonify(todo)

# DELETE /api/todos/<int:todo_id> - Delete a todo
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    if todo_id not in todos_store:
         return jsonify({"error": "Todo not found"}), 404

    del todos_store[todo_id]
    # Return No Content status
    return '', 204

# --- Run the App ---
if __name__ == '__main__':
    # Runs on http://127.0.0.1:5000 by default
    # Use host='0.0.0.0' to make it accessible on your network
    app.run(debug=True, port=5000) # debug=True enables auto-reloading