from concurrent.futures import ThreadPoolExecutor as PE
from boto3.exceptions import S3UploadFailedError
import boto3


class S3Adapter:
    def __init__(self, bucket, bulk_size=100, verbose=False):
        self.__client = boto3.client('s3')
        self.__bucket = bucket
        self.__bulk_size = bulk_size
        self.__verbose = verbose

    def process(self, payload):
        stats = {'total': len(payload), 'successes': [], 'errors': []}
        with PE(max_workers=self.__bulk_size) as executor:
            for response in executor.map(self.__upload, payload):
                if response['status'] == False:
                    stats['errors'].append(response)
                elif response['status'] == True:
                    stats['successes'].append(response)

        return stats

    def __upload(self, item):
        key = item['destination']
        try:
            body = item['body']
            response = self.__client.put_object(Bucket=self.__bucket, Key=key, Body=body, ContentType=item['content-type'])
            if self.__verbose:
                print('[info] Uploaded successfully - key: "{}"'.format(key))

            response = {
                'type': 's3',
                'bucket': self.__bucket,
                'key': key,
                'status_code': response['ResponseMetadata']['HTTPStatusCode']
            }
            if response['status_code'] == 200:
                response['status'] = True

            return response
        except S3UploadFailedError as e:
            print('[error] ', e)

            return {'type': 's3', 'error': e, 'key': key, 'bucket': self.__bucket, 'status': False}
