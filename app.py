from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join("data", "tasks.json")


def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks):
    """Generate the next task ID."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


@app.route("/")
def home():
    return {"message": "Task Management API is running!"}


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return {"error": "Task not found!"}, 404
    return jsonify(task)


@app.route("/tasks", methods=["POST"])
def create_task():
    tasks = load_tasks()
    data = request.get_json()

    if "title" not in data:
        return {"error": "Title is required!"}, 400

    new_task = {
        "id": get_next_id(tasks),
        "title": data["title"],
        "description": data.get("description", ""),
        "status": data.get("status", "pending")
    }

    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return {"error": "Task not found!"}, 404

    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["status"] = data.get("status", task["status"])

    save_tasks(tasks)
    return jsonify(task)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return {"error": "Task not found!"}, 404

    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return {"message": "Task deleted successfully!"}


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)

    app.run(debug=True)
