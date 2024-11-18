import zmq
import random
from openpyxl import load_workbook
from collections import deque


# Load quotes from the Excel file
def load_quotes(file_path):
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active  # Use the first sheet
        # Read all non-empty cells in column A
        quotes = [cell.value for cell in sheet["A"] if cell.value]
        return quotes
    except Exception as e:
        print("Error loading quotes:", e)
        return []


# Function to get a random quote
def get_random_quote(quotes, recent_quotes):
    while True:
        quote = random.choice(quotes)
        if quote not in recent_quotes:
            # Add the quote to the recent list and maintain a max size of 50
            recent_quotes.append(quote)
            if len(recent_quotes) > 50:
                recent_quotes.popleft()  # Remove the oldest quote
            return quote


# ZeroMQ server
def start_server(file_path):
    # Load the quotes from the Excel file
    quotes = load_quotes(file_path)
    if not quotes:
        print("No quotes found in the Excel file.")
        return

    # Start a deque where there can be maximum 50 quotes stored
    recent_quotes = deque(maxlen=50)

    # Create a ZeroMQ context
    context = zmq.Context()

    socket = context.socket(zmq.REP)  # Create a REP socket
    socket.bind("tcp://*:5555")  # Connect to port 5555

    print("Random Quote Generator microservice is running...")

    while True:
        # Wait for a request
        message = socket.recv_string()

        if message == "GET_RANDOM_QUOTE":
            # Get a random quote and send it back
            quote = get_random_quote(quotes, recent_quotes)
            socket.send_string(quote)
        else:
            # Handle unknown requests
            socket.send_string("Unknown request. Please send 'GET_RANDOM_QUOTE'.")


if __name__ == "__main__":
    quotes_file = "fitness-quotes.xlsx"
    start_server(quotes_file)
