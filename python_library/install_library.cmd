python setup.py bdist_wheel
pip uninstall -y imclas
pip install -r requirements.txt dist\imclas-0.1-py2-none-any.whl