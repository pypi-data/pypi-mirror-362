from setuptools import setup, find_packages

setup(
    name='tvpulse',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
    ],
    author='SDIO',
    author_email='dev@sdio.io',
    description='Official TVPulse SDK for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sdio/tvpulse-python-sdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
