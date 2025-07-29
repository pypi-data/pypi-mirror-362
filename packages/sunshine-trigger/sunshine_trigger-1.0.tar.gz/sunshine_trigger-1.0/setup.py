from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='sunshine-trigger',
    version='1.0',
    author='Christophe Godart',
    author_email='51CGO@lilo.org',
    description='Tool for executing commands on sunrise and sunset',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/51CGO/python-sunshine-trigger",
    packages=find_packages(),
    install_requires=[
        'suntimes',
    ],
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
)