import ftplib


def anonlogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('root', 'hx1NM396')
        print('\n[*]' + str(hostname) + 'ftp successed!')
        ftp.quit()
        return True
    except Exception as e:
        print('failded to ftp' + str(hostname))
        return False


if __name__ == '__main__':
    anonlogin('154.221.18.35')