from concurrent.futures import ThreadPoolExecutor as PE
import boto3, mimetypes

class S3Adapter:
    bulksize = 50

    def __init__(self, bucket, bulksize=50):
        self.client = boto3.client('s3')
        self.bucket = bucket
        self.bulksize = bulksize

    def process(self, payload):
        it = 0
        successes = 0
        errors = 0
        with PE(max_workers=self.bulksize) as executor:
            for response in executor.map(self.upload, payload):
                if response == False:
                    errors += 1
                else:
                    successes += 1

                it += 1

        return it, successes, errors

    def upload(self, item):
        try:
            key = item['destination']
            body = item['body']
            self.client.put_object(Bucket=self.bucket, Key=key, Body=body, ContentType=item['content-type'])
            print('[info] Uploaded successfully - key: "{}"'.format(key))

            return True
        except Exception as e:
            print('[error] ', e)

            return False
