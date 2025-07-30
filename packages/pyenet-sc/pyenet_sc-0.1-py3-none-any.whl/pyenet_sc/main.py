import enet
import json

class Request:
    def __init__(self, requestId, requestData):
        self.requestId = requestId
        self.requestData = requestData

    def serialize(self):
        return json.dumps({
            'requestId': self.requestId,
            'requestData': self.requestData
        }).encode()

    @staticmethod
    def deserialize(data):
        obj = json.loads(data.decode())
        return Request(obj['requestId'], obj['requestData'])

class Client:
    def __init__(self, client, peer):
        self.client = client
        self.peer = peer
        self.doNetworking = True

    def send_data(self, event, data):
        self.peer.send(0, enet.Packet(data, enet.PACKET_FLAG_RELIABLE))
    def recieve_data(self, event):
        if event.type == enet.EVENT_TYPE_RECEIVE:
            return [event.packet.data, event.peer.address]
        return None
    
    def update(self, onSelfConnect, doEach):
        if self.doNetworking:   
            event = self.client.service(0)
            if event.type == enet.EVENT_TYPE_CONNECT:
                onSelfConnect(event)
            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                print("Disconnected from server")
                self.doNetworking = False
            else:
                doEach(event)

class Server:
    def __init__(self, port, onConnect, onDisconnect, onRecv):
        self.host = None
        self.onConnect = onConnect
        self.onDisconnect = onDisconnect
        self.onRecv = onRecv
        self.port = port
    
    def send_data(self, event, data):
        event.peer.send(0, enet.Packet(data, enet.PACKET_FLAG_RELIABLE))
    def recieve_data(self, event):
        if event.type == enet.EVENT_TYPE_RECEIVE:
            return [event.packet.data, event.peer.address]
        return None
    
    def mainloop(self):
        self.host = enet.Host(enet.Address(b'localhost', self.port), 32, 2, 0, 0)

        print(f"ENet server started on port {self.port}")

        while True:
            event = self.host.service(0)  # wait up to 1000 ms for an event
            if event.type == enet.EVENT_TYPE_CONNECT:
                # print(f"Client connected from {event.peer.address}")
                # event.peer.send(0, enet.Packet(b"Welcome!", enet.PACKET_FLAG_RELIABLE))
                self.onConnect(event)

            elif event.type == enet.EVENT_TYPE_RECEIVE:
                # print(f"Received: {event.packet.data} from {event.peer.address}")
                # # Echo back the data
                # event.peer.send(0, event.packet)
                self.onRecv(event)

            elif event.type == enet.EVENT_TYPE_DISCONNECT:
                # print(f"Client disconnected: {event.peer.address}")
                self.onDisconnect(event)

class InternetHandler:
    @staticmethod
    def setup_client(ip, port):
        client = enet.Host(None, 1, 2, 0, 0)
        server_address = enet.Address(ip.encode('utf-8'), port)
        peer = client.connect(server_address, 2)

        print("Connecting to server...")
        return Client(client, peer)