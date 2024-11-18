import zmq
import wikipedia
import time

# Set up ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Wikipedia microservice listening on port 5555")

while True:
    time.sleep(1)
    # Receive request from client
    request = socket.recv_string()
    print(f"Received request: {request}")

    # Query Wikipedia API for page type, if no page found, return not found
    search = wikipedia.suggest(request)
    if search == None:
        socket.send_string("not found")
        continue

    # Send "what type?" response
    socket.send_string("what type?")

    # Receive second request from client
    type = socket.recv_string()
    print(f"Received second request: {type}")

    # Query Wikipedia API for summary or image
    if type == "summary":
        # if receive request for summary, return summary up to 10 sentences.
        socket.send_string(wikipedia.summary(search, sentences=10))
    elif type == "photo":
        photos = wikipedia.images(search)
        if len(photos) > 0:
            socket.send_string(photos[0])
    else:
        socket.send_string("Invalid request")