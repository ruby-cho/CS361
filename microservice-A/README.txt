# Random Quote Generator Microservice

This repository implements a Random Quote Generator Microservice using ZeroMQ. The microservice provides a random quote from a provided set of motivational, fitness-related quotes stored in an Excel file. The service makes sure that no quote from the last 50 generated quotes is repeated.

---

## Communication Contract

    1. Protocol: ZeroMQ REQ-REP 
    2. Request Format:
        The client sends a string message: "GET_RANDOM_QUOTE".
        No other form of string message will work. (See below)
    3. Response Format:
        The server replies with a string containing the quote. (See below)

---

## How to Request / Receive Data 

To request data, the client must:

    1. Connect to the server's endpoint (tcp://localhost:5555, but port can be changed).
    2. Send the message: "GET_RANDOM_QUOTE".

To receive data, the client must: 

    1. Remember that the quote will be in simple string form (ex: "Work harder, stronger, faster.")
    2. Store result and print it in a location that it sees fit.

Code snippet: 

    ```import zmq

    def request_random_quote():
        # Create a ZeroMQ context
        context = zmq.Context()

        # Create a REQ (Request) socket
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")  # Connect to the server

        # Send the request
        socket.send_string("GET_RANDOM_QUOTE")

        # Receive the response
        quote = socket.recv_string()
        print("Received Quote:", quote)

    if __name__ == "__main__":
        request_random_quote()```

--- 

## Notes

* Server expects the following form for query: "GET_RANDOM_QUOTE"
* Server sends back the quote in single string form: "Quote Quote Quote"
* If client wants to add more quotes to the batch, add directly to Excel file.




