# PyEnetRequestServerClient

This library is a simple wrapper around the enet library  
It provides easier client and server creation and also request structure.  
Check the example

# Creating a server

```py
from pyenet_sc import *

# This function will run when a client connects
def onConnect(event):
    # event.peer.address is the clients address
    print(f"Client connected from {event.peer.address}")

    # Sending a request to every client that connects once
    r = Request("msg", {"text": "Hello, Client!"})
    server.send_data(event, r.serialize())

# This function will run when a client disconnects
def onDisconnect(event):
    print(f"Client disconnected: {event.peer.address}")

# This is the main server function which handles recieving and sending requests
def onRecv(event):
    # Get any sent data
    data = server.recieve_data(event)
    if data:
        # Get request from the data
        raw, address = data
        request = Request.deserialize(raw)
        print(f"From {address}: Request({request.requestId}, {request.requestData})")

# Initialize our server
server: Server = Server(24337, onConnect, onDisconnect, onRecv)
server.mainloop()
```

# Creating a client

```py
from pyenet_sc import *

# Create a client and connect it to a server
client: Client = InternetHandler.setup_client('127.0.0.1', 24337)

# This will run when the client is connected to a server
def onSelfConnect(event):
    r = Request("msg", {"text": "Hello Server!"})
    client.send_data(event, r.serialize())

# This handles sending and recieving requests between this client and the server
def onEach(event):
    data = client.recieve_data(event)
    if data:
        raw, address = data
        request = Request.deserialize(raw)
        print(f"From {address}: Request({request.requestId}, {request.requestData})")

# client.update doesnt have a mainloop it expects to be ran in the mainloop of the program
while True:
    client.update(onSelfConnect, onEach)
```
