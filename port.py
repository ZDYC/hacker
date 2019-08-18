import optparse
import socket
from socket import *
import queue as Queue
from threading import Thread


def scan_port(host, i, queue):
    while True:
        port = queue.get()
        try:
            conn_skt = socket(AF_INET, SOCK_STREAM)
            conn_skt.connect(host, port)
            conn_skt.send('python')
            results = conn_skt.recv(100)
            print('[+]%d tcp open' % port)
            print('[+] ' + str(results))
            conn_skt.close()
            queue.task_done()
        except Exception:
            print('port %s/tcp closed' % port)
            # pass
# def conn_scan(tgt_host, tgt_port):
#     try:
#         conn_skt = socket(AF_INET, SOCK_STREAM)
#         conn_skt.connect((tgt_host, tgt_port))
#         conn_skt.send("python")
#         results = conn_skt.recv(100)
#         print('[+]%d tcp open' % tgt_port)
#         print('[+] ' + str(results))
#         conn_skt.close()
#     except Exception:
#         print('[-]%d/tcp closed' % tgt_port)


# def port_scan(tgt_host, tgt_ports):
#     try:
#         tgt_ip = gethostbyname(tgt_host)
#     except:
#         print('[-] can not resolve %s unkown host' % tgt_host)
#         return
#     try:
#         tgt_name = gethostbyaddr(tgt_ip)
#         print('\n[+] scan results for;' + tgt_name[0])
#     except:
#         print('\n[+] scan results for;' + tgt_ip)
#     setdefaulttimeout(1)
#     for tgt_port in tgt_ports:
#         print('scaning port ' + tgt_port)
#         conn_scan(tgt_host, int(tgt_port))

def main():
    #     # port_scan(tgt_host, tgt_ports)
    parser = optparse.OptionParser('usage%prog ' + "-H <host> -p <port>")
    parser.add_option('-H', dest='host', type='string', help='specify host')
    parser.add_option('-p', dest='port', type='string', help='specify port')
    options, args = parser.parse_args()
    host = options.host
    ports = str(options.port).split(', ')
    if host is None:
        print('error host')
        exit(0)
    if ports is None:
        ports = [i for i in range(1, 1000)]
    num_threads = 5
    q = Queue.Queue()
    for i in range(num_threads):
        t = Thread(target=scan_port, args=(host, i, q))
        t.setDaemon(True)
        t.start()

    for port in ports:
        q.put(port)
    print('main threading waiting....')
    q.join()
    print('done')


if __name__ == '__main__':
    main()
    # print(gethostbyname('www.baidu.com'))
    # print(gethostbyname('154.221.18.35'))
    # print(gethostbyaddr('14.215.177.39'))
