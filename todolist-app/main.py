# main.py

import zmq
import json
from menu import main_menu  # Importing the main_menu function from menu.py


def main():

    print("\n\n")
    print("--------------------------------------------------------------------")
    print("Welcome to My To Do List App!")
    print("\nKeep track of your tasks using a simple To-do list app.")
    print("Add/Edit/Delete tasks, and check stats to increase your productivity!")
    print('\nAt any point in this app, input "b" to return to previous page.\n')
    print("--------------------------------------------------------------------")

    # Set up ZeroMQ context and socket PORT = 5555
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while True:
        print("Say or type your password to start:")
        print('If new user, type "new":')

        # Get user input
        user_input = input("> ")

        # Prepare and send JSON message
        message = {"action": "auth", "data": user_input}
        socket.send_json(message)

        # Receive and process response from the authentication microservice
        response = socket.recv_json()
        print(response["message"])

        # If prompted to set a new password, handle that input
        if response["message"] == "Enter a new password:":
            new_password = input("> ")
            socket.send_json({"action": "auth", "data": new_password})

            # Final confirmation response
            confirmation_response = socket.recv_json()
            print(confirmation_response["message"])
            print("\nPlease enter your password to start:")

        elif response["message"] == "Authentication successful! Welcome back.":
            socket.send_json({"action": "exit"})
            print(
                "--------------------------------------------------------------------"
            )
            main_menu()
            break


if __name__ == "__main__":
    main()
