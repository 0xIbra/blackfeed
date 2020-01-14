from concurrent.futures import ThreadPoolExecutor as PE
from boto3.exceptions import S3UploadFailedError
import boto3, mimetypes

class S3Adapter:
    bulksize = 50

    def __init__(self, bucket, bulksize=50, verbose=False):
        self.client = boto3.client('s3')
        self.bucket = bucket
        self.bulksize = bulksize
        self.verbose = verbose

    def process(self, payload):
        stats = { 'total': len(payload), 'successes': [], 'errors': [] }
        with PE(max_workers=self.bulksize) as executor:
            for response in executor.map(self.upload, payload):
                if response['status'] == False:
                    stats['errors'].append(response)
                elif response['status'] == True:
                    stats['successes'].append(response)

        return stats

    def upload(self, item):
        key = item['destination']
        try:
            body = item['body']
            response = self.client.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType=item['content-type'])
            if self.verbose:
                print('[info] Uploaded successfully - key: "{}"'.format(key))

            response = {
                'type': 's3',
                'bucket': self.bucket,
                'key': key,
                'status_code': response['ResponseMetadata']['HTTPStatusCode']
            }
            if response['status_code'] == 200:
                response['status'] = True

            return response
        except S3UploadFailedError as e:
            print('[error] ', e)

            return { 'type': 's3', 'error': e, 'key': key, 'bucket': self.bucket, 'status': False }
