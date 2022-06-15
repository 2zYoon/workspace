# server

import rpyc

if __name__ == '__main__':
    conn = rpyc.connect("localhost", 33333)
    x = conn.root.foo(10)
    print(x)