import socket
import sys


def banner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect(ip, port)
        banner = s.recv(1024)
        return banner
    except:
        return

portLists = [21, 24, 25, 80, 110, 443]
for port in portLists:
    print(banner('154.221.18.35', port))


if len(sys.argv) == 2:
    filename = sys.argv[1]
    print(filename)
