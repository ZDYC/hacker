from threading import Thread
import subprocess
import queue as Queue
from socket import gethostbyaddr

import netifaces
import nmap

def get_name(ip):
    nmScan = nmap.PortScanner()
    nmScan.scan(hosts=ip, arguments='-sP')
    print(nmScan._scan_result)
    # if nmScan[ip]['hostnames'][0]['name']:
    #     return {'IP Address:': ip,
    #             'Hostname:': nmScan[ip]['hostnames'][0]['name']
    #            }


def get_gateways():
    return netifaces.gateways()['default'][netifaces.AF_INET][0]


def get_ip_lists(gateways):
    ip = gateways.split('.')
    return [ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + str(i) for i in range(0, 257)]


def ping(i, queue):
    while True:
        ip = queue.get()
        res = subprocess.call('ping -c 1 %s' % ip, shell=True,
                              stdout=open('/Users/yu/Desktop/projects/hacker/null', 'w'),
                              stderr=subprocess.STDOUT)
        if res == 0:
            print(get_name(ip))
            print(ip, 'alive')
        queue.task_done()


def main():
    num_threads = 100
    q = Queue.Queue()
    for i in range(num_threads):
        t = Thread(target=ping, args=(i, q))
        t.setDaemon(True)
        t.start()

    for ip in get_ip_lists(get_gateways()):
        q.put(ip)
    print('main thread waiting..')
    q.join()
    print('done!')


if __name__ == '__main__':
    main()
