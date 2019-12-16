from concurrent.futures import ThreadPoolExecutor as PE
import requests

class Downloader:
    bulksize = 50
    session = None

    def __init__(self, adapter, multi=False, bulksize=50):
        self.adapter = adapter
        self.bulksize = bulksize
        self.multi = multi
        self.session = requests.session()
        self.stats = {
            'total_images': 0,
            'downloads': 0,
            'uploads': 0,
            'errors': 0
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
                        if not response.ok:
                            self.stats['errors'] += 1
                            print('[error] Could not download file: "{}"'.format(item['url']))
                            continue

                        adapter_queue.append({
                            'destination': item['destination'],
                            'body': response.content,
                            'content-type': response.headers['Content-Type']
                        })

                self.adapter.process(adapter_queue)
                adapter_queue = []

        if len(download_queue) > 0:
            with PE(max_workers=self.bulksize) as executor:
                for request in executor.map(self.download, download_queue):
                    item = request['item']
                    response = request['response']
                    if not response.ok:
                        print('[error] Could not download file: "{}"'.format(item['url']))
                        continue

                    adapter_queue.append({
                        'destination': item['destination'],
                        'body': response.content,
                        'content-type': response.headers['Content-Type']
                    })

            self.adapter.process(adapter_queue)
            adapter_queue = []


    def handle(self, queue):
        upload_queue = []
        for item in queue:
            try:
                response = self.download(item)
                downloaded = response['response']
                if not downloaded.ok:
                    print('[error] Could not download file: "{}"'.format(item['url']))
                    continue

                upload_queue.append({
                    'destination': item['destination'],
                    'body': downloaded.content,
                    'content-type': downloaded.headers['Content-Type']
                })
            except Exception as e:
                print('[error]', e)

        try:
            print('[info] Starting to execute adapter...')
            self.adapter.process(upload_queue)
        except Exception as e:
            print('[error]', e)

    def download(self, item):
        if self.session is None:
            self.session = requests.session()

        try:
            headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3' }
            url = item['url']

            return { 'item': item, 'response': self.session.get(url, headers=headers) }
        except Exception as e:
            print('[error]', e)

            return False

    def get_stats(self):
        return self.stats