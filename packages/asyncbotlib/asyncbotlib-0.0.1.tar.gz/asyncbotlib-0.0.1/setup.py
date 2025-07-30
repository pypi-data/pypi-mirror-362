from setuptools import setup, find_packages

setup(
    name='asyncbotlib',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'aiohttp'
    ],
    author='winxp_dev_2',
    author_email='db3006177@gmail.com',
    description='Async+Sync Telegram Bot Framework',
    license='MIT',
    keywords='telegram'
)