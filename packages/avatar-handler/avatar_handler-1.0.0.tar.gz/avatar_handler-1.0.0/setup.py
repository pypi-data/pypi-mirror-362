from setuptools import setup, find_packages

setup(
    name='avatar_handler',
    version='1.0.0',
    author='A.H. Team',
    description='A library for handling and setting user avatars from various sources.',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Pillow',
    ],
) 