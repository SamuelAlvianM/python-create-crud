from flask import Flask, request, jsonify
from flask.views import MethodView
import uuid

app = Flask(__name__)

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
    },
        "3": {
        "id": "3",
        "title": "Practice RUST",
        "description": "Review RUST fundamentals.",
        "completed": False
    },
        "4": {
        "id": "4",
        "title": "Practice GOLANG",
        "description": "Review GOLANG fundamentals.",
        "completed": False
    }
}

class TaskAPI(MethodView):
    def get(self, task_id=None):

        if task_id:

            task = tasks_db.get(task_id)
            if task:
                return jsonify(task)
            return jsonify({"error": "Task not found"}), 404
        else:

            return jsonify(list(tasks_db.values()))
    
    def post(self):

        data = request.get_json()
        
        if not data or not 'title' in data:
            return jsonify({"error": "Title is required"}), 400
        
        task_id = str(uuid.uuid4())[:8] 
        new_task = {
            "id": task_id,
            "title": data.get("title"),
            "description": data.get("description", ""),
            "completed": False
        }
        
        tasks_db[task_id] = new_task
        return jsonify(new_task), 201
    
    def put(self, task_id):

        if not task_id or task_id not in tasks_db:
            return jsonify({"error": "Task not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        task = tasks_db[task_id]

        if 'title' in data:
            task['title'] = data['title']
        if 'description' in data:
            task['description'] = data['description']
        
        return jsonify({"message": "Task updated successfully."})
    
    def delete(self, task_id):
        """Handle DELETE requests to remove a task"""
        if not task_id or task_id not in tasks_db:
            return jsonify({"error": "Task not found"}), 404
        
        del tasks_db[task_id]
        return jsonify({"message": "Task deleted successfully."})
    
    def patch(self, task_id):

        if not task_id or task_id not in tasks_db:
            return jsonify({"error": "Task not found"}), 404
        
        tasks_db[task_id]['completed'] = True
        return jsonify({"message": "Task marked as completed."})

task_view = TaskAPI.as_view('task_api')
app.add_url_rule('/tasks', view_func=task_view, methods=['GET', 'POST'])
app.add_url_rule('/tasks/<task_id>', view_func=task_view, methods=['GET', 'PUT', 'DELETE'])
app.add_url_rule('/tasks/<task_id>/complete', view_func=task_view, methods=['PATCH'])

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