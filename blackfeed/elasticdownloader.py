from urllib.parse import urlparse
import re

class ElasticDownloader:

    def download(self, uri, localpath=None):
        if not re.search(r'\w+:(\/?\/?)[^\s]+', uri):
            raise Exception('[error] Invalid URI "{}"'.format(uri))

        self.parsed = urlparse(uri)
        scheme = self.parsed.scheme
        payload = self.prepare_uri(uri)
        if scheme == 'http' or scheme == 'https':
            from blackfeed.helper.http_download import download

            return download(uri, localpath)
        elif scheme == 'ftp':
            from blackfeed.elastic.ftp import FTP

            if 'port' not in payload:
                payload['port'] = 21

            ftp = FTP(payload['host'], payload['user'], payload['password'], payload['port'])
            res = ftp.download(payload['path'], localpath)
            if res != False:
                print('[info] File downloaded')
                print('[info] File path: "{}"'.format(res))

            ftp.close()

            return res
        elif scheme == 'sftp':
            from blackfeed.elastic.sftp import SFTP

            if 'port' not in payload:
                payload['port'] = 22

            sftp = SFTP(payload['host'], payload['user'], payload['password'], payload['port'])
            res = sftp.download(payload['path'], localpath)
            if res != False:
                print('[info] File downloaded - Path: "{}"'.format(res))

            sftp.close()

            return res
        else:
            raise Exception('[error] Unsupported scheme "{}"'.format(scheme))

    def retrieve(self, uri):
        if not re.search(r'\w+:(\/?\/?)[^\s]+', uri):
            raise Exception('[error] Invalid URI "{}"'.format(uri))

        self.parsed = urlparse(uri)
        scheme = self.parsed.scheme
        payload = self.prepare_uri(uri)
        if scheme == 'http' or scheme == 'https':
            from blackfeed.helper.http_download import retrieve

            return retrieve(uri)
        elif scheme == 'ftp':
            from blackfeed.elastic.ftp import FTP

            if 'port' not in payload:
                payload['port'] = 21

            ftp = FTP(payload['host'], payload['user'], payload['password'], payload['port'])
            res = ftp.retrieve(payload['path'])
            if res != False:
                print('[info] File downloaded')
                print('[info] File path: "{}"'.format(res))

            ftp.close()

            return res
        elif scheme == 'sftp':
            from blackfeed.elastic.sftp import SFTP

            if 'port' not in payload:
                payload['port'] = 22

            sftp = SFTP(payload['host'], payload['user'], payload['password'], payload['port'])
            res = sftp.retrieve(payload['path'])
            if res != False:
                print('[info] File downloaded - Path: "{}"'.format(res))
            
            sftp.close()

            return res
        else:
            raise Exception('[error] Unsupported scheme "{}"'.format(scheme))

    def prepare_uri(self, uri):
        self.parsed = urlparse(uri)
        payload = {}

        netloc = self.parsed.netloc
        if '@' in netloc:
            split = netloc.split('@')
            creds = split[0]
            server = split[1]

            if ':' in server:
                splitserver = server.split(':')
                server = splitserver[0]
                port = splitserver[1]

                payload['host'] = server
                payload['port'] = int(port)
            else:
                payload['host'] = server

            if ':' in creds:
                credsplit = creds.split(':')
                user = credsplit[0]
                password = credsplit[1]

                payload['user'] = user
                payload['password'] = password
            else:
                payload['password'] = creds

        payload['path'] = self.parsed.path

        return payload