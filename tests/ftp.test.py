from blackfeed.elasticdownloader import ElasticDownloader

uri = 'ftp://demo-user:demo-user@demo.wftpserver.com/download/manual_en.pdf'

retriever = ElasticDownloader()
res = retriever.retrieve(uri)

print(res)