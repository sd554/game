# Simple Python Network Library
# author: Andrew Merrill
# version: 0.3 beta 4

import socket, threading, struct, Queue, time

DEFAULT_NETWORK_PORT = 8000

################################################################################            
# use this function on the client side
# server is the name of the server computer (use 'localhost' to talk to yourself)
# the server must have already run the listen function before you run this
# this returns a NetworkConnection object
#  but it returns None if it cannot connect to the server
def connect(server, port=DEFAULT_NETWORK_PORT):
    try:
        mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        mysocket.connect((server,port))
        return NetworkConnection(mysocket)
    except socket.error:
        return None

################################################################################
# use this function on the server side
# the new_client_function takes one argument: NetworkConnection
# when a client connects, your new_client_function will get called
def listen(new_client_function, port=DEFAULT_NETWORK_PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)
    
    def wait_for_clients():
        while True:
            (client_socket, address) = server_socket.accept()
            new_client_function(NetworkConnection(client_socket))
                        
    return start_thread(wait_for_clients)

def get_local_ipaddr():
    #return socket.gethostbyname(socket.gethostname())
    addrs = socket.gethostbyname_ex(socket.gethostname())[2]
    for addr in addrs:
        if addr[:3] != '127':
            return addr
    return addr[0]


def get_local_name():
    return socket.gethostname()



################################socket.recv################################################
# you never make objects of this class by yourself
# instead, use the connect or listen functions (above)
class NetworkConnection:
    def __init__(self, mysocket):
        self.socket = mysocket
        (self.remote_name, self.remote_port) = self.socket.getpeername()
        (self.local_name, self.local_port) = self.socket.getsockname()
        self.receive_message_function = None
        self.disconnect_message_function = None
        self.is_alive = True
        self.incoming_queue = Queue.Queue()
        self.outgoing_queue = Queue.Queue()
        self.receive_thread = start_thread(self._receive_messages)
        self.send_thread = start_thread(self._send_messages)
  
    # use this to send a message
    #  returns true if server is still connected
    #  returns false if server connection is dead
    def send(self, message):
        message = str(message)
        self.outgoing_queue.put(message)
        return self.send_thread.is_alive()

    # returns True if at least one incoming message has been received
    def has_messages(self):
        return not self.incoming_queue.empty()
    
    # returns the first unread incoming message (as a string)
    def get_message(self, timeout=None):
        try:
            return self.incoming_queue.get(True, timeout)
        except Queue.Empty:
            return None
    
    # this is used to register a function that will get called when
    #    an incoming message arrives
    # receive_message_function takes two arguments: NetworkConnection, message
    def on_receive(self, receive_message_function):
        self.receive_message_function = receive_message_function
        if receive_message_function is not None:
            while self.has_messages():
                self.receive_message_function(self, self.incoming_queue.get())
                
    def on_disconnect(self, disconnect_message_function):
        self.disconnect_message_function = disconnect_message_function
    
    # use this to close the NetworkConnection when you are done with it
    def close(self):
        self.socket.close()
        
    def get_remote_ipaddr(self):
        return self.remote_name
    
    def get_remote_name(self):
        return socket.gethostbyaddr(self.remote_name)[0]
        
    # this function is for internal use only
    # it is the body of the send_thread
    # it loops forever, processing outgoing messages
    def _send_messages(self):
        try:
            while True:
                message = self.outgoing_queue.get()
                prefix = struct.pack('H', len(message))
                self.socket.sendall(prefix + message)
        except socket.error:
            self.is_alive = False
            if self.disconnect_message_function is not None:
                self.disconnect_message_function(self)

    # this function is for internal use only
    # it is the body of the receive_thread
    # it loops forever, processing incoming messages
    def _receive_messages(self):
        try:
            while True:
                message_len_packed = self._receive_bytes(2)
                if message_len_packed is None:
                    break
                (message_len,) = struct.unpack('H', message_len_packed)
                message = self._receive_bytes(message_len)
                if message is None:
                    break
                if self.receive_message_function is None:
                    self.incoming_queue.put(message)
                else:
                    self.receive_message_function(self, message)
        except socket.error:
            pass
        self.is_alive = False
        if self.disconnect_message_function is not None:
            self.disconnect_message_function(self)

    # this function is for internal use only
    # this reads and returns the given number of bytes
    #   this waits until that many bytes have been received, which
    #   could be a very long time
    def _receive_bytes(self, length):
        message = ''
        message_len = 0
        while message_len < length:
            new_message = self.socket.recv(length-message_len)
            if not new_message:
                return None
            message += new_message
            message_len += len(new_message)
        return message

#################################################################################
def start_thread(run_function):
    thread = threading.Thread(target=run_function)
    thread.daemon = True
    thread.start()
    return thread

#################################################################################
# waits forever
def wait():
    while True:
        time.sleep(60)
