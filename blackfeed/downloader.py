from concurrent.futures import ThreadPoolExecutor as PE
from requests import session as RequestSession
from requests.exceptions import RequestException

class Downloader:
    bulksize = 50
    session = None

    def __init__(self, adapter, multi=False, bulksize=50):
        self.adapter = adapter
        self.bulksize = bulksize
        self.multi = multi
        self.session = RequestSession()
        self.stats = {
            'total_images': 0,
            'downloads': {
                'total_successes': 0,
                'total_errors': 0,
                'successes': [],
                'errors': []
            },
            'uploads': {
                'total_successes': 0,
                'total_errors': 0,
                'successes': [],
                'errors': []
            }
        }

    def process(self, queue):
        self.stats['total_images'] = len(queue)
        if self.multi == False:
            self.handle(queue)
        else:
            self.handle_multi(queue)

    def handle_multi(self, queue):
        download_queue = []
        adapter_queue = []
        for item in queue:
            download_queue.append(item)
            if (len(download_queue) % self.bulksize) == 0:
                with PE(max_workers=self.bulksize) as executor:
                    for request in executor.map(self.download, download_queue):
                        item = request['item']
                        response = request['response']
                        if not response['status']:
                            self.stats['downloads']['errors'].append(response)
                            self.stats['downloads']['total_errors'] += 1
                            print('[error] Could not download file: "{}"'.format(item['url']))
                            continue

                        adapter_queue.append({
                            'destination': item['destination'],
                            'body': response['content'],
                            'content-type': response['headers']['Content-Type']
                        })

                        self.stats['downloads']['successes'].append(response)
                        self.stats['downloads']['total_successes'] += 1

                stats = self.adapter.process(adapter_queue)
                self.handle_upload_stats(stats)
                adapter_queue = []

        if len(download_queue) > 0:
            with PE(max_workers=self.bulksize) as executor:
                for request in executor.map(self.download, download_queue):
                    item = request['item']
                    response = request['response']
                    if not response['status']:
                        self.stats['downloads']['errors'].append(response)
                        self.stats['downloads']['total_errors'] += 1

                        print('[error] Could not download file: "{}"'.format(item['url']))

                        continue

                    adapter_queue.append({
                        'destination': item['destination'],
                        'body': response['content'],
                        'content-type': response['headers']['Content-Type']
                    })

                    self.stats['downloads']['successes'].append({
                        'url': response['url'],
                        'httpcode': response['httpcode'],
                        'status': response['status'],
                        'headers': response['headers']
                    })
                    self.stats['downloads']['total_successes'] += 1

            stats = self.adapter.process(adapter_queue)
            self.handle_upload_stats(stats)
            adapter_queue = []

    def handle(self, queue):
        # Handles downloads without multithreading

        upload_queue = []
        for item in queue:
            try:
                download = self.download(item)
                http_response = download['response']
                if not http_response['status']:
                    print('[error] Could not download file: "{}"'.format(item['url']))
                    self.stats['downloads']['errors'].append(http_response)
                    self.stats['downloads']['total_errors'] += 1

                    continue

                upload_queue.append({
                    'destination': item['destination'],
                    'body': http_response['content'],
                    'content-type': http_response['headers']['Content-Type']
                })

                self.stats['downloads']['successes'].append({
                    'url': http_response['url'],
                    'httpcode': http_response['httpcode'],
                    'status': http_response['status'],
                    'headers': http_response['headers']
                })
            except Exception as e:
                print('[error]', e)

        try:
            if len(upload_queue) <= 0:
                print('[warning] S3 Upload queue is empty')

                return False

            print('[info] Starting to execute adapter...')
            stats = self.adapter.process(upload_queue)
            self.handle_upload_stats(stats)

        except Exception as e:
            print('[error]', e)

    def download(self, item):
        # Downloads a single file and returns the HTTP response

        if self.session is None:
            self.session = RequestSession()

        try:
            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3' }
            url = item['url']
            request = self.session.get(url, headers=headers)
            response = {
                'url': url,
                'httpcode': request.status_code,
                'status': request.ok,
                'headers': request.headers
            }
            if request.ok:
                response['content'] = request.content

            return { 'item': item, 'response': response }
        except RequestException as e:
            print('[error]', e)

            return { 'item': item, 'response': { 'status': False, 'error': e, 'url': item['url'] } }

    def handle_upload_stats(self, stats):
        total_successes = len(stats['successes'])
        total_errors = len(stats['errors'])
        self.stats['uploads']['total_successes'] += total_successes
        self.stats['uploads']['total_errors'] += total_errors

        for success in stats['successes']:
            self.stats['uploads']['successes'].append(success)
        
        for error in stats['errors']:
            self.stats['uploads']['errors'].append(error)

    def get_stats(self):
        return self.stats

    def append_stats(self, stats):
        pass