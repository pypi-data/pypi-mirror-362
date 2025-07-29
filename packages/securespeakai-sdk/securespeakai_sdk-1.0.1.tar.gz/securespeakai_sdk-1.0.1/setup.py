from setuptools import setup, find_packages

setup(
    name='securespeakai-sdk',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'websocket-client>=1.2.0',
        'typing-extensions>=4.0.0',
        'pyaudio>=0.2.11'
    ],
    description='SecureSpeakAI Python SDK for deepfake detection with comprehensive API support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='SecureSpeakAI',
    author_email='nsharma@securespeakai.com',
    url='https://securespeakai.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
    ],
    python_requires='>=3.7',
    keywords='deepfake detection, audio analysis, AI, machine learning, api, sdk',
    project_urls={
        'Documentation': 'https://securespeakai.com/docs',
        'Homepage': 'https://securespeakai.com',
        'Support': 'https://securespeakai.com/support',
    },
) 