import json
from datetime import datetime

TOKEN_FILE = ".github/token_usage.json"
DAILY_LIMIT = 100

def get_token_count():
    """Reads the token file and returns the current token count."""
    try:
        with open(TOKEN_FILE, "r") as f:
            data = json.load(f)
            return data.get("tokens_used", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def increment_token_count():
    """Increments the token count in the token file."""
    count = get_token_count()
    if count < DAILY_LIMIT:
        count += 1
        today = datetime.now().strftime("%Y-%m-%d")
        with open(TOKEN_FILE, "w") as f:
            json.dump({"date": today, "tokens_used": count}, f)
    return count

def reset_token_count():
    """Resets the token count to 0 and updates the date."""
    today = datetime.now().strftime("%Y-%m-%d")
    with open(TOKEN_FILE, "w") as f:
        json.dump({"date": today, "tokens_used": 0}, f)

TASK_QUEUE_FILE = ".github/task_queue.json"

def add_task_to_queue(task):
    """Adds a task to the task queue."""
    try:
        with open(TASK_QUEUE_FILE, "r") as f:
            queue = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        queue = []
    queue.append(task)
    with open(TASK_QUEUE_FILE, "w") as f:
        json.dump(queue, f)

def get_tasks_from_queue():
    """Retrieves all tasks from the task queue."""
    try:
        with open(TASK_QUEUE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Note: Using a JSON file for state management is not robust for high-traffic repositories
# and can be prone to race conditions. For a more scalable solution, consider using a
# dedicated database or a service like GitHub's own storage for Actions.

def remove_task_from_queue(task):
    """Removes a specific task from the task queue."""
    try:
        with open(TASK_QUEUE_FILE, "r") as f:
            queue = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        queue = []

    new_queue = [t for t in queue if t != task]

    with open(TASK_QUEUE_FILE, "w") as f:
        json.dump(new_queue, f)

def clear_task_queue():
    """Clears all tasks from the task queue."""
    with open(TASK_QUEUE_FILE, "w") as f:
        json.dump([], f)

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "get":
            print(get_token_count())
        elif command == "increment":
            increment_token_count()
        elif command == "reset":
            reset_token_count()
        elif command == "add_task":
            add_task_to_queue(json.loads(sys.argv[2]))
        elif command == "get_tasks":
            print(json.dumps(get_tasks_from_queue()))
        elif command == "remove_task":
            remove_task_from_queue(json.loads(sys.argv[2]))
        elif command == "clear_queue":
            clear_task_queue()
