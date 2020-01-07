from blackfeed.elasticdownloader import ElasticDownloader

uri = 'sftp://foo:pass@127.0.0.1:22/data/notes.txt'

retriever = ElasticDownloader()
# res = retriever.retrieve(uri)

# with open('notes.txt', 'wb') as fh:
#     fh.write(res.getvalue())

retriever.download(uri, '.')