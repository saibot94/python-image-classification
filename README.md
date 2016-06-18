### Python Image Classification
#### Bachelor's thesis project - West University of Timisoara

This project sets out to implement a generic image classification library that can take a training dataset of images and learn to  identify if they belong to a certain category or not. It comes with an API as well as a Web interface, so that the user can see similarities and other metrics after training a model.

Requirements:

- numpy
- scipy
- sklearn


#### Installation:

To install the library, one must have a running Ubuntu or Debian-based environment and run __install_dependencies.sh__.

You can also install it on Windows, providing you install the above libraries before running __instsall_library.cmd__.
I suggest not using virtualenvs when installing on windows.

The install script works if you start by creating a virtual environment, by doing the following:

* sudo apt-get install virtualenv
* virtualenv --system-site-packages virtualenv

After that, run __install_library.sh__ and you will have the __imclas__ package built in the library.


