from setuptools import setup, find_packages

setup(
    name='kroxzyapi',
    version='1.0.0',
    description='Kroxzy sistemine otomatik bağlantı modülü',
    author='kroxzy',
    author_email='kroxzy91@gmail.com',
    packages=find_packages(),
    install_requires=['requests']
)