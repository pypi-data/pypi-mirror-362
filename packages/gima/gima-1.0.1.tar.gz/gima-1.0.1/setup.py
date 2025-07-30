from setuptools import setup

setup(
    name='gima',
    version='1.0.1',
    author='Arkadiusz Hypki',
    description='Software which simplifies managing many git repositories through a console',
    packages=['gim'],
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'pygit2'
    ],
)