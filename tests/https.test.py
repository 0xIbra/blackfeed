from blackfeed.elasticdownloader import ElasticDownloader

uri = 'https://i.picsum.photos/id/881/800/600.jpg'

retriever = ElasticDownloader()
# retriever.download(uri, '.')

res = retriever.retrieve(uri)
print(res)

with open('image.jpg', 'wb') as fh:
    fh.write(res.getvalue())