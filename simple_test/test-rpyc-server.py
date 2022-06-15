# server

import rpyc
from rpyc.utils.server import ThreadedServer

class A(rpyc.Service):
    def __init__(self):
        self.a = 10
    def exposed_foo(self, x):
        return self.a + x

if __name__ == '__main__':
    server = ThreadedServer(A, port=33333)
    server.start()
