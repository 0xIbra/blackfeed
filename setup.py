import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='blackfeed',
    version='0.0.7',
    author='Ibragim Abubakarov',
    author_email='ibragim.ai95@gmail.com',
    description='A micro python library that allow the download of thousands of files concurrently',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ibragim64/downloader',
    packages=['blackfeed'],
    install_requires=['requests', 'boto3'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)