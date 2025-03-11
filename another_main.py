from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Dummy database - a simple dictionary to store tasks
tasks_db = {
    "1": {
        "id": "1",
        "title": "Learn Flask",
        "description": "Build an API using Flask.",
        "completed": False
    },
    "2": {
        "id": "2",
        "title": "Practice Python",
        "description": "Review Python fundamentals.",
        "completed": True
    }
}

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify(list(tasks_db.values()))

# Get a specific task by ID
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks_db.get(task_id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if not data or not 'title' in data:
        return jsonify({"error": "Title is required"}), 400
    
    task_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
    new_task = {
        "id": task_id,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "completed": False
    }
    
    tasks_db[task_id] = new_task
    return jsonify(new_task), 201

# Update a task
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks_db:
        return jsonify({"error": "Task not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    task = tasks_db[task_id]
    
    # Update task fields
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    
    return jsonify({"message": "Task updated successfully."})

# Delete a task
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id not in tasks_db:
        return jsonify({"error": "Task not found"}), 404
    
    del tasks_db[task_id]
    return jsonify({"message": "Task deleted successfully."})

# Mark a task as completed (Bonus)
@app.route('/tasks/<task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    if task_id not in tasks_db:
        return jsonify({"error": "Task not found"}), 404
    
    tasks_db[task_id]['completed'] = True
    return jsonify({"message": "Task marked as completed."})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)