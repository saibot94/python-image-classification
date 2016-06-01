from setuptools import setup, find_packages

setup(name='imclas',
      version='0.1',
      description='Python General Image Classification Library',
      author='Cristian Schuszter',
      author_email='chrisschuszter@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(),
      requires=["sklearn", "numpy", "matplotlib"]
      )
