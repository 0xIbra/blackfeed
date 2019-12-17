# Downloader
> Downloader is a micro python library that allows you download and upload (S3, GCS, etc...)
> with/without multithreading.

### Packages required
- requests
- boto3

## Usage
Download and upload files to AWS S3
**For this to work, AWS CLI must be configured**
```python
from dtf.downloader import Downloader
from dtf.adapter.s3 import S3Adapter

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
    bulksize=200 # Number of concurrent downloads
)
downloader.process(queue)
stats = downloader.get_stats() # Returns a dict with informations about the process
```