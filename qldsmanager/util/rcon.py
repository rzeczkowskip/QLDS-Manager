import zmq
import uuid
import struct
import sys
import threading
import queue
import re


class Rcon:
    def __init__(self, host, port, password):
        self.context = None
        self.socket = None
        self.monitor = None
        self.__queue = None
        self.identity = uuid.uuid1().hex.encode()

        self.host = host
        self.port = port
        self.password = password

    def connect(self):
        self.__queue = self.__input()

        self.context = zmq.Context()

        self.socket = self.context.socket(zmq.DEALER)
        self.monitor = self.socket.get_monitor_socket(zmq.EVENT_ALL)

        self.socket.plain_username = b'rcon'
        self.socket.plain_password = self.password.encode()
        self.socket.zap_domain = b'rcon'

        self.socket.setsockopt(zmq.IDENTITY, self.identity)

        self.socket.connect('tcp://%s:%s' % (self.host, self.port))

    def loop(self):
        event = self.socket.poll(100)
        event_monitor = self.__monitor()

        if event_monitor is not None:
            if event_monitor[0] == zmq.EVENT_CONNECTED:
                self.socket.send(b'register')
                print('Connected to %s:%s' % (self.host, self.port))
            elif event_monitor[0] == zmq.EVENT_CLOSED:
                print('Could not connect to %s:%s' % (self.host, self.port))
                print('Check if host, post and password are valid')
                return False

        prev = None
        while not self.__queue.empty():
            line = self.__queue.get()

            if prev != line:
                self.socket.send_string(line)
                print('rcon: %s' % line)
                prev = line

        if event == 0:
            return True

        while True:
            try:
                msg = self.__parse_msg(self.socket.recv(zmq.NOBLOCK))
            except zmq.error.Again:
                break
            except Exception as e:
                print(e)
                break
            else:
                if msg is not None:
                    print(msg, end='')

        return True

    def __monitor(self):
        try:
            event_monitor = self.monitor.recv(zmq.NOBLOCK)
        except zmq.Again:
            return

        event_id = struct.unpack('<H', event_monitor[:2])[0]
        event_value = struct.unpack('<I', event_monitor[2:])[0]

        self.monitor.recv(zmq.NOBLOCK)

        return [event_id, event_value]

    def __input(self):
        def wait_for_stdin(queue__):
            while True:
                input_ = sys.stdin.readline()
                if len(input_) > 1:
                    queue__.put(input_)

        queue_ = queue.Queue()

        thread = threading.Thread(target=wait_for_stdin, args=[queue_])
        thread.daemon = True
        thread.start()

        return queue_

    def __parse_msg(self, msg: bytes):
        msg = msg.decode()

        if msg.startswith('zmq RCON command from %s' % self.identity.decode()):
            return

        if msg.startswith('broadcast: print'):
            msg = re.sub(r'broadcast: print \"(.+)\\n\"', r'\1', msg)

        if msg.startswith('print "') and msg.endswith('\n"'):
            msg = re.sub(r'print \"(.+)\n\"', r'\1', msg) + '\n'

        return re.sub('\^.', '', msg)
