import json
import threading
import time
import methods

class RobotConnection(threading.Thread):
    '''Thread that runs the connection with the robot and does actions according to the messages'''
    def __init__(self, connection, server):
        threading.Thread.__init__(self)
        self.connection = connection
        self.server = server
        self.message_queue = [] #we shouldnt need this but incase 2 messages are entered at the same time this will cathc that 

    def run(self):
        #startup sequence where the server and robot do a handshake on that they are ready for comm
        json_message = {'type':'ready_for_communication', 'value':True}
        self.sent(json_message)
        json_message = self.receive()
        if json_message['type'] == 'ready_for_communication' and json_message['value'] == True:
            #self.connection.settimeout(2.0) #set timeout to 2 seconds of waiting before it continues with the code
            while True:
                json_message = ''
                json_message = self.receive()
                if json_message['type'] == 'ready':
                    if json_message['value'] == True:
                        self.server.server_processes.robot_ready = True        
                elif json_message['type'] == 'arrived_at_target':
                    if json_message['value'] == 'ready':
                        self.server.server_processes.robot_at_shelve = True
                while not self.message_queue:
                    for message in self.message_queue:
                        self.sent(message)
                    
        error_message = 'robot did not send the correct message, see log for last received message'
        methods.print_log(error_message)
        print(error_message)
    
    def receive(self):
        message = self.connection.recv(4096)
        message = methods.decrypt(message)
        
        methods.print_log('robot - {}'.format(message)) #might remove the replace if using minimalistic json convertion
        return json.loads(message)

    def sent(self, message):
        message = json.dumps(message, separators=(',',':'))
        methods.print_log('server - {}'.format(message))
        
        message = methods.encrypt(message)
        self.connection.sendall(message)

class DatabaseHook(threading.Thread):

    def __init__(self, server_processes):
        threading.Thread.__init__(self)
        self.server_processes = server_processes

    def run(self):
        old_time = time.time()
        new_time = time.time()
        while not self.server_processes.robot_ready:
            pass
        while True:
            new_time = time.time() #time in seconds
            if new_time - old_time >= 5:
                old_time = new_time
                update_processes = False
                update_order_items = False
                tray_values = self.server_processes.db_connector.get_query('SELECT products.name, products.amount_in_stock, products.id, productsinshelve.shelf_id, productsinshelve.x_coordinate, productsinshelve.y_coordinate FROM productsinshelve LEFT JOIN products ON products.id = productsinshelve.product_id WHERE amount_in_cartridge < 1')
                #check if items in this
                if tray_values != (): #TODO check if this is the empty list representation
                    for item in tray_values:
                        if item not in self.server_processes.trays_to_replace:
                            self.server_processes.trays_to_replace.append(item)
                            update_processes = True

                tray_values = self.server_processes.db_connector.get_query('SELECT id, name, amount_in_stock FROM products WHERE amount_in_stock < 20')
                if tray_values != ():
                    for item in tray_values:
                        #print(item, self.server_processes.items_to_order)
                        if item not in self.server_processes.items_to_order:
                            if not update_order_items:
                                self.server_processes.items_to_order = []
                            self.server_processes.items_to_order.append(item)
                            update_order_items = True
                            update_processes = True
                if update_processes:    
                    self.server_processes.tray_list_updated()
