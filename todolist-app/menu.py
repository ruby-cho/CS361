# menu.py

import zmq
import json
import os

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")  # Connects to add_item_service on port 5555


# load existing categories
def load_categories():
    """Load categories from a JSON file (categories.txt)."""
    with open("categories.txt", "r") as f:
        return json.load(f)


# print out menu for users to read from
def display_menu():
    print("\nChoose from the Menu:")
    print("Type one of the following options:")
    print("\t1. Add item")
    print("\t2. View to-do list")
    print("\t3. Listen to to-do list")
    print("\t4. View Stats")
    print("\t5. Exit")
    print('At any point in this app, input "b" to return to previous page.\n')
    print(
        "Going back while adding/editing a task may result in progress not being saved."
    )
    print("--------------------------------------------------------------------")


# add item
def add_item():
    print("\n[Add item]\n")
    print("At any point in this app, input 'b' to return to previous page.")
    task = input(
        "Type what task you want to add, and we’ll add that to a category automatically: "
    )
    print("\n")
    date = input("For what date? (MM/DD/YYYY): ")
    print("\n")

    socket.send_json(
        {"action": "add_item", "task": task, "date": date, "confirm_category": True}
    )

    # Wait for category confirmation response
    response = socket.recv_json()
    if response["status"] == "confirm_category":
        print(response["message"])

        # Step 2: Get user confirmation
        user_confirmation = input().strip().lower()
        if user_confirmation == "n":
            categories = load_categories()
            for category in categories.keys():
                print(f" - {category}")
            user_category = input("Enter the correct category from the above:")
            socket.send_json({"confirm": "n", "user_category": user_category})
        else:
            socket.send_json({"confirm": "y"})

        # Wait for final response
        final_response = socket.recv_json()
        print(final_response["message"])

    # Ask if user wants to add another item
    want_another = input("Want to add another? (y/n): ").strip().lower()
    if want_another == "y":
        print("------------------------------------------------------")
        add_item()  # Call add_item again

    # Show user the todo list if they want to see it
    see_todo_list = input("Want to see the list? (y/n): ").strip().lower()
    if see_todo_list == "y":
        view_todo_list()


TASKS_FILE = "tasks.json"


# view to do list
def view_todo_list():

    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks_list = json.load(file)

    if not tasks_list:
        print("Your to-do list is currently empty.")
    else:
        print("\nYour To-Do List:")
        for item in tasks_list:
            print(
                f"Task: {item['task']}, Date: {item['date']}, Category: {item['category']}"
            )


def listen_todo_list():
    print("\n[Listen to To-Do List]")
    print("To be implemented")


def view_stats():
    print("\n[View Stats]")
    print("To be implemented")


def main_menu():
    display_menu()
    while True:
        choice = input("> ").strip()

        if choice == "1":
            add_item()
        elif choice == "2":
            view_todo_list()
        elif choice == "3":
            listen_todo_list()
        elif choice == "4":
            view_stats()
        elif choice == "5":
            confirm_choice = input(
                "Are you sure you want to exit? Some progress might be lost: (y/n)"
            )
            if confirm_choice == "y":
                print("\nExiting the application. Goodbye!")
                break
        elif choice.lower() == "b":
            print("\nReturning to the previous page...")
            break
        else:
            print("Invalid option. Please try again.")
