from requests import session as RequestSession
from requests.exceptions import RequestException
from io import BytesIO
import os, tempfile

def download(url, localpath=None):
    filename = os.path.basename(url)
    localfilepath = os.path.join(tempfile.gettempdir(), filename)
    if localpath is not None and os.path.isdir(localpath):
        localfilepath = os.path.join(localpath, filename)

    session = RequestSession()
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3' }
    request = session.get(url, headers=headers)

    if not request.ok:
        return False

    with open(localfilepath, 'wb') as fh:
        fh.write(request.content)

    return localfilepath

def retrieve(url):
    session = RequestSession()
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3' }
    request = session.get(url, headers=headers)

    if not request.ok:
        return False

    res = BytesIO()
    res.write(request.content)

    return res