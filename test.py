from downloader import Downloader
from adapter.s3 import S3Adapter

payload = [
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi.jpg'
    },
    {
        'url': 'https://publicar-medias-dev.s3.eu-west-3.amazonaws.com/audi.jpg',
        'filename': 'audi.jpg',
        'destination': 'somedir/audi_1.jpg'
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

downloader = Downloader(S3Adapter(bucket='publicar-dev'), multi=True)
stats = downloader.process(payload)
