from setuptools import setup, find_packages

setup(
    name='securespeakai-sdk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests'],
    description='SecureSpeakAI Python SDK for deepfake detection',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='SecureSpeakAI',
    author_email='nsharma@securespeakai.com',
    url='https://securespeakai.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
) 