from io import BytesIO
import pysftp, os, tempfile

class SFTP:

    def __init__(self, host, user=None, password=None, port=22):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.client = pysftp.Connection(host, username=user, password=password, port=port, cnopts=cnopts)

    def download(self, path, localpath=None):
        filename = os.path.basename(path)
        localfilepath = os.path.join(tempfile.gettempdir(), filename)
        if localpath is not None and os.path.isdir(localpath):
            localfilepath = os.path.join(localpath, filename)

        if not self.client.isfile(path):
            return False

        try:
            self.client.get(path, localfilepath)

            if not os.path.isfile(localfilepath):
                return False

            return localfilepath
        except Exception as e:
            print('[error] ', e)

            return False

    def retrieve(self, path):
        binarycontent = BytesIO()
        if not self.client.isfile(path):
            print('[error] File "{}" does not exist on remote server'.format(path))
            return False

        try:
            self.client.getfo(path, binarycontent)
        except Exception as e:
            print('[error] ', e)

            return False

        return binarycontent

    def close(self):
        self.client.close()