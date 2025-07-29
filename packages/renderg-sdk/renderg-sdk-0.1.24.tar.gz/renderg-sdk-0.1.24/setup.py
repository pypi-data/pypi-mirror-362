from os import path

from setuptools import setup, find_packages


def get_readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(
    name='renderg-sdk',
    version='0.1.24',
    url='https://github.com/renderg-repo/renderg-sdk.git',
    author='RenderG',
    author_email='support@renderg.com',
    description='www.renderg.com',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),    
    install_requires=[
        'requests',
        'tenacity',
        'paho-mqtt'
    ],
    package_data={
        'analyze_houdini': ["./houdini/*"],
        'ascp': ["./*/*"],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
