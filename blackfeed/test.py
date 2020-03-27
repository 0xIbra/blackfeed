from downloader import Downloader
from adapter.s3 import S3Adapter
import json

payload = [
    {
        'url': 'https://www.businessinsider.fr/content/uploads/2019/03/-1536-1152.jpg',
        'filename': 'ferrari.jpg',
        'destination': 'ferrari/458/ferrari-458.jpg'
    },
    {
        'url': 'http://img.over-blog-kiwi.com/1/40/60/51/20190113/ob_b4f71a_lamborghini-huracan-evo-2019-101.jpg',
        'filename': 'lamborghini.jpg',
        'destination': 'lamborghini/lamborghini-huracan.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_2.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_3.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_4.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_5.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_6.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_7.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_8.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_9.jpg'
    }
]


def callback(queue):
    print("QUEUE: ", queue)


downloader = Downloader(S3Adapter(bucket='publicar-dev'), multi=True, stateless=False, state_id='states')

downloader.set_callback(callback)

# downloader.load_states('states')
downloader.process(payload)
stats = downloader.get_stats()

print('STATS', stats)

# File = open('output.json', 'w')
# File.write(json.dumps(stats))
# File.close()