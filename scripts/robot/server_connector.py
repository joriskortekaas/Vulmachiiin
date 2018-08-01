import socket
import json
from encryptor import Encryptor
from IO_controller import IO_controller

class Server_Connector:

    encryptor = Encryptor()
    iocontroller = IO_controller()

    def __init__(self, IP_address, port):
        print('Creating socket')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP_address = IP_address
        self.port = port

    def run(self):
        self.s.connect((self.IP_address, self.port))
        print('Succesfully connected to: ', self.IP_address)
        # Send a 1 to the server to let it know that you're a robot
        self.send('1')
        message = self.s.receive(1024)
        json_message = {'ready': True}
        self.send(json_message)
        while True:
            message = self.receive()
            if(message['type'] == 'route'):
                directions = message['routes']
                for directionlist in directions:
                    for direction in directionlist:
                        print('Next direction: ' + direction)
                        while(self.iocontroller.detect_node() == "line"):
                            pass
                        if(self.iocontroller.detect_node() == "node"):
                            # TODO draai naar dirction
                            print("Node detected")
                            #self.iocontroller.control_motors(directions)

    def send(self, message):
        jsonmessage = json.dumps(message)
        encryptedmessage = self.encryptor.encrypt(jsonmessage)
        self.s.send(encryptedmessage)

    def receive(self):
        receivedmessage = self.s.recv(1024)
        receivedmessage = self.encryptor.decrypt(receivedmessage)
        return json.loads(receivedmessage)
