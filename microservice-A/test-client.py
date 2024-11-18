# test-client.py
# Test program for the random quote generator.

import zmq

# Create a ZeroMQ context
context = zmq.Context()

# Create a REQ socket
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")  # Connect to the microservice at port 5555

# Send request for a random quote
print("Sent a reqeust to the random quote generator microservice.")
socket.send_string("GET_RANDOM_QUOTE")

# Wait for the response
response = socket.recv_string()
print("\nHere's the quote:", response)  # Test print of the quote
