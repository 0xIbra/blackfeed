# BlackFeed
> BlackFeed is a micro python library that allows you download and upload files concurrently.
> You can download your files locally but you can also upload them to your cloud without writing them to disk.

### Packages required
> Installed automatically with **pip**
- requests
- boto3

## Install
```bash
pip install blackfeed
```

## Usage
Download and upload files to AWS S3
**For this to work, AWS CLI must be configured**
```python
from blackfeed.downloader import Downloader
from blackfeed.adapter.s3 import S3Adapter

queue = [
    {
        'url': 'https://www.example.com/path/to/image.jpg', # Required
        'destination': 'some/key/image.jpg' # S3 key - Required 
    },{
        'url': 'https://www.example.com/path/to/image2.jpg',
        'destination': 'some/key/image2.jpg' 
    }
]

downloader = Downloader(
    S3Adapter(bucket='bucketname'),
    multi=True, # If true, uploads files to images to S3 with multithreading
    stateless=False # If set to False, it generates and stores md5 hashes of files in a file
    state_id='flux_states' # name of the file where hashes will be stored (states.txt) not required
    bulksize=200 # Number of concurrent downloads
)
downloader.process(queue)
stats = downloader.get_stats() # Returns a dict with information about the process
```

### Download files with states
Loading states can be useful if you don't want to re-download the same file twice.
```python
from blackfeed.downloader import Downloader
from blackfeed.adapter.s3 import S3Adapter

queue = [
...
]

downloader = Downloader(
    S3Adapter(bucket='bucketname'),
    multi=True,
    stateless=False,
    state_id='filename'
)
downloader.load_states('filename') # This will load states from "filename.txt"
downloader.process(queue)
stats = downloader.get_stats() # Statistics 
```

## ElasticDownloader
> Let's you to download/retrieve files from FTP, SFTP and HTTP/S servers easily.

### Examples
#### Downloading file from FTP 
```python
from blackfeed.elasticdownloader import ElasticDownloader

uri = 'ftp://user:password@ftp.server.com/path/to/file.csv'

retriever = ElasticDownloader()
res = retriever.download(uri, localpath='/tmp/myfile.csv') # localfile is optional
# .download() function returns False if there was an error or return the local path of the downloaded file if it was a success.
print(res)
```
```bash
/tmp/myfile.csv
```

### Retrieving binary content of file from FTP
```python
from blackfeed.elasticdownloader import ElasticDownloader

uri = 'ftp://user:password@ftp.server.com/path/to/file.csv'

retriever = ElasticDownloader()
res = retriever.retrieve(uri) # Return type: io.BytesIO | False

with open('/tmp/myfile.csv', 'wb') as f:
    f.write(res.getvalue())
```
**ElasticDownloader** can handle FTP, SFTP and HTTP URIs automatically.
Use the method **download** to download file locally and use the **retrieve** method to get the binary content of a file.