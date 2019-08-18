import pdb
import optparse
import queue as Queue
from threading import Thread

import requests


def parser():
    parser = optparse.OptionParser('usage%prog ' + '-P <proxy>')
    parser.add_option('-P', dest='proxy', type='string', help='specify proxy host')
    (options, args) = parser.parse_args()
    return options.proxy


def download(proxy, i, queue):
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
    while True:
        url = queue.get()
        try:
            res = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=5, headers=headers)
        except requests.RequestException as e:
            print('requests {} error {}!'.format(url, e))
        else:
            if res.status_code == 200:
                print('success request {}'.format(url))
            queue.task_done()


def main():
    # proxy = 'http://' + parser()
    proxy = 'http://127.0.0.1:1087'
    urls = ['http://185.38.13.130//mp43/331268.mp4?st=U6zO0cFBILZ0DQ0nN6KsGg&e=1566187487',
            'http://185.38.13.130//mp43/331271.mp4?st=LYeVsK-LPGnVTboyyJ7cmg&e=1566187493'
            ]
    num_threads = 2
    q = Queue.Queue()
    for i in range(num_threads):
        t = Thread(target=download, args=(proxy, i, q))
        t.setDaemon(True)
        t.start()

    for url in urls:
        q.put(url)
    print('main threading waiting....')
    q.join()
    print('done!')


if __name__ == '__main__':
    # parser()
    main()