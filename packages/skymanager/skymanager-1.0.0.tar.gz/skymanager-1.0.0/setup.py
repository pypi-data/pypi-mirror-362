import os
import codecs

from setuptools import setup, find_packages


VERSION = '1.0.0'
DESCRIPTION = 'Asynchronous api of the SkyManager service'

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='skymanager',
    version=VERSION,
    author='Mits',
    author_email='<mits.dev.tg@gmail.com>',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['aiohttp', 'cachetools'],
    keywords=['python', 'skymanager', 'async', 'asyncio', 'cache'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ],
    url='https://github.com/MitsCreator/skymanagerapi',
    project_urls={
        'Homepage': 'https://github.com/MitsCreator/skymanagerapi',
        'Bug Tracker': 'https://github.com/MitsCreator/skymanagerapi/issues',
    },
)