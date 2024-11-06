import zmq
import json
import os

# file where password is stored
PASSWORD_FILE = "password.txt"


# save password to file
def save_password(password):
    with open(PASSWORD_FILE, "w") as file:
        file.write(password)


# load existing password from file
def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return file.read().strip()
    return None


# authenticate the user
def authenticate_user(input_password):
    saved_password = load_password()

    # if no password exists, ask for a new password
    if saved_password is None:
        return "No password set. Type 'new' to create a password."

    # compare saved password with entered password
    elif input_password == saved_password:
        return "Authentication successful! Welcome back."
    else:
        return "Invalid password. Try again."


def main():
    # Set up ZeroMQ context and socket PORT = 5555
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Authentication service is running...")

    while True:
        try:
            # Wait for a request for authentication
            message = socket.recv_json()
            action = message.get("action")
            data = message.get("data")

            # make appropriate actions based on request content
            if action == "auth":
                # if requesting for a new password to be created
                if data == "new":
                    if load_password() is None:
                        response = {"message": "Enter a new password:"}
                        socket.send_json(response)

                        # Wait for the user to send a new password
                        new_password_message = socket.recv_json()
                        new_password = new_password_message.get("data")
                        save_password(new_password)
                        response = {"message": "Password set successfully!"}
                    else:
                        response = {
                            "message": "Password already set. Please authenticate."
                        }
                # actually authenticate user
                else:
                    response = {"message": authenticate_user(data)}

            # if authentication is complete, end service
            elif action == "exit":
                response = {"message": "Exiting authentication service."}
                socket.send_json(response)
                break  # Exit the while loop to end the service

            # Send the response back to the main CLI
            socket.send_json(response)

        # if there's an exception, exit loop
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    # close socket when authentication is complete
    socket.close()
    context.term()
    print("Authentication service has stopped.")


if __name__ == "__main__":
    main()
