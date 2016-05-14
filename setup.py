from setuptools import setup



setup(name='imclas',
      version='0.1',
      description='Python General Image Classification Library',
      author='Cristian Schuszter',
      author_email='chrisschuszter@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['imclas'],
      requires=["sklearn", "numpy", "matplotlib"]
     )

