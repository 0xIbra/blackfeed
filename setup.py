import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='blackfeed',
    version='0.0.9',
    author='Ibragim Abubakarov',
    author_email='ibragim.ai95@gmail.com',
    description='A python package that allows the download of thousands of files concurrently',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ibragim64/blackfeed',
    packages=['blackfeed', 'blackfeed.adapter', 'blackfeed.helper', 'blackfeed.elastic'],
    install_requires=['requests', 'boto3', 'pysftp'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)