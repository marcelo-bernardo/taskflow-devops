from flask import Flask, jsonify, request

app = Flask(__name__)
tasks = []
next_id = 1


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/tasks")
def list_tasks():
    return jsonify(tasks)


@app.post("/tasks")
def create_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="title e obrigatorio"), 400
    task = {"id": next_id, "title": title, "done": False}
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201


def find_task(task_id):
    return next((t for t in tasks if t["id"] == task_id), None)


@app.put("/tasks/<int:task_id>")
def complete_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify(error="tarefa nao encontrada"), 404
    task["done"] = True
    return jsonify(task)


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    task = find_task(task_id)
    if task is None:
        return jsonify(error="tarefa nao encontrada"), 404
    tasks.remove(task)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
