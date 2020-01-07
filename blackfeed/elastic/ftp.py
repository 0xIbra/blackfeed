from ftplib import FTP as FTPSession
from io import BytesIO
import os, tempfile

class FTP:

    def __init__(self, host, user=None, password=None, port=21):
        self.client = FTPSession()
        self.client.connect(host, port)
        if user is not None and password is not None:
            self.client.login(user, password)

    def download(self, path, localpath=None):
        directory = os.path.dirname(path)
        filename  = os.path.basename(path)
        localfilepath = os.path.join(tempfile.gettempdir(), filename)

        if localpath is not None and localpath != '':
            if os.path.isdir(localpath):
                localfilepath = os.path.join(localpath, filename)

        if directory != '':
            self.client.cwd(directory)
        
        try:
            output = self.client.retrbinary('RETR ' + filename, open(localfilepath, 'wb').write)
            if not output.startswith('226'):
                # raise Exception('[error] Could not download file from FTP')
                print('[error] Could not download file')
                print('[error] Output: {}'.format(output))

                return False

            return localfilepath
        except Exception as e:
            # raise Exception('[error] ', e)
            print('[error] ', e)

            return False

    def retrieve(self, path):
        directory = os.path.dirname(path)
        filename = os.path.basename(path)

        if directory != '':
            self.client.cwd(directory)
        
        try:
            binarycontent = BytesIO()
            cmd = 'RETR {}'.format(filename)
            self.client.retrbinary(cmd, binarycontent.write)

            return binarycontent
        except Exception as e:
            print('[error] ', e)

            return False

    def close(self):
        self.client.close()