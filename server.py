from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os

TASKS_FILE = "tasks.txt"

TASKS = []
NEXT_TASK_ID = 1


def load_tasks():
    global TASKS, NEXT_TASK_ID
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                TASKS = data.get("tasks", [])
                NEXT_TASK_ID = data.get("next_id", 1)
                for task in TASKS:
                    task["isDone"] = bool(task.get("isDone", False))
        except Exception as e:
            print(f"Ошибка при загрузке tasks.txt: {e}")
            TASKS = []
            NEXT_TASK_ID = 1


def save_tasks():
    try:
        data = {
            "tasks": TASKS,
            "next_id": NEXT_TASK_ID
        }
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении в tasks.txt: {e}")


class TodoRESTHandler(BaseHTTPRequestHandler):

    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length) if length > 0 else b""
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _send_json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _error(self, status, msg):
        self._send_json({"error": msg}, status=status)

    def do_POST(self):
        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.split("/") if p]

        if len(parts) == 1 and parts[0] == "tasks":
            self.create_task()
        elif len(parts) == 3 and parts[0] == "tasks" and parts[2] == "complete":
            self.complete_task(parts[1])
        else:
            self._error(404, "Not found")

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/tasks":
            self.list_tasks()
        else:
            self._error(404, "Not found")

    def create_task(self):
        global NEXT_TASK_ID
        data = self._read_json_body()

        if not data or "title" not in data or "priority" not in data:
            return self._error(400, "Fields 'title' and 'priority' are required")

        priority = data["priority"]
        if priority not in {"low", "normal", "high"}:
            return self._error(400, "Priority must be one of: low, normal, high")

        task = {
            "id": NEXT_TASK_ID,
            "title": data["title"],
            "priority": priority,
            "isDone": False
        }
        TASKS.append(task)
        NEXT_TASK_ID += 1

        save_tasks()
        self._send_json(task, 201)

    def list_tasks(self):
        self._send_json(TASKS)

    def complete_task(self, task_id_str):
        try:
            task_id = int(task_id_str)
        except ValueError:
            return self._error(400, "Task id must be integer")

        for task in TASKS:
            if task["id"] == task_id:
                task["isDone"] = True
                save_tasks()  # Сохраняем после изменения
                self.send_response(200)
                self.end_headers()
                return

        self._error(404, "Task not found")


def run(host="127.0.0.1", port=8000):
    load_tasks()
    print(f"Serving on http://{host}:{port}")
    server = HTTPServer((host, port), TodoRESTHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    run()