import zmq
import json
import os

TASKS_FILE = "tasks.json"


# Load existing tasks from JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []


# Save a new task to the JSON file
def save_task(task_item):
    tasks = load_tasks()
    tasks.append(task_item)
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)


# Load existing categories from categories.txt file
# format: {"Daily": ["buy", "do"], "Shopping": ["shop", "buy"]}
def load_categories():
    with open("categories.txt", "r") as f:
        return json.load(f)


# "Detect" categories based on keywords from the task
def detect_category(task, categories):
    for category, keywords in categories.items():
        if any(keyword.lower() in task.lower() for keyword in keywords):
            return category
    # if no category has been detected, return default category (Daily)
    return "Daily"


# ZeroMQ setup for response socket PORT: 5556
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")


# add task item to to-do list
def main():
    while True:
        # Wait for request from main.py
        message = socket.recv_json()
        if message["action"] == "add_item":
            categories = load_categories()
            task = message["task"]  # assign task
            date = message["date"]  # assign date

            # get suggested category
            suggested_category = detect_category(task, categories)

        # Send suggested category back for user confirmation
        confirm_category = {
            "status": "confirm_category",
            "task": task,
            "date": date,
            "suggested_category": suggested_category,
            "message": f'Suggested category: "{suggested_category}". Confirm? (y/n)',
        }
        socket.send_json(confirm_category)

        # Wait for confirmation response
        confirm_message = socket.recv_json()
        if confirm_message.get("confirm") == "n":
            category = confirm_message.get("user_category", suggested_category)
        else:
            category = suggested_category

        # Create a new todo item
        todo_item = {"task": task, "date": date, "category": category}

        # Save todo item to task list
        save_task(todo_item)

        # Send a final response back to main.py
        final_response = {
            "status": "success",
            "message": f'Successfully added "{task}" to "{category}" on {date}.',
        }
        socket.send_json(final_response)


if __name__ == "__main__":
    main()
