import json
from IO_controller import IO_controller
import socket
import wiringpi
import methods
import time

class Server_Connector:

    def __init__(self, IP_address, port):
        print('Creating socket')
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP_address = IP_address
        self.port = port
        wiringpi.wiringPiSetupGpio()
        self.iocontroller = IO_controller(23,24)

    def run(self):
        self.s.connect((self.IP_address, self.port))
        print('Succesfully connected to: ', self.IP_address)
        # Send a 1 to the server to let it know that you're a robot
        self.s.send(b'1')
        message = self.s.recv(1024)
        json_message = {'type': 'ready_for_communication', 'value': True}
        self.send(json_message)
        while True:
            json_message = {'type': 'ready', 'value': True}
            self.send(json_message)
            message = self.receive()
            if(message['type'] == 'route'):
                directions = message['routes']
                for directionlist in directions:
                    '''for direction in directionlist:
                        print('Next direction: ' + direction)
                        while(self.iocontroller.detect_node() == "line"):
                            pass
                        if(self.iocontroller.detect_node() == "node"):
                            # TODO draai naar dirction
                            print("Node detected")
                            # self.iocontroller.control_motors(directions)'''
                    time.sleep(3)
                    print('at shelve')
                    self.send({'type': 'arrived_at_target', 'value': 'ready'})

    def send(self, message):
        jsonmessage = json.dumps(message)
        print(jsonmessage)
        encryptedmessage = methods.encrypt(jsonmessage)
        self.s.send(encryptedmessage)

    def receive(self):
        receivedmessage = self.s.recv(1024)
        receivedmessage = methods.decrypt(receivedmessage)
        print(receivedmessage)
        return json.loads(receivedmessage)


server_connector = Server_Connector('80.56.122.76', 54321)
server_connector.run()
