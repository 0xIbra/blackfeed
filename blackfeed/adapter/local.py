from concurrent.futures import ThreadPoolExecutor as PE
import os


class LocalAdapter:
    def __init__(self, bulk_size=50, verbose=False):
        self.__bulk_size = bulk_size
        self.__verbose = verbose

    def process(self, payload):
        stats = {'total': len(payload), 'successes': [], 'errors': []}
        with PE(max_workers=self.__bulk_size) as executor:
            for result in executor.map(LocalAdapter.write_local, payload):
                if not result['status']:
                    print(f"[error] could not save image: {result['destination']}")

        return stats

    @staticmethod
    def write_local(item):
        local_path = item['destination']
        body = item['body']
        with open(local_path, 'wb') as f:
            f.write(body)
        was_file_saved = os.path.isfile(local_path)

        return {'destination': local_path, 'status': was_file_saved}
