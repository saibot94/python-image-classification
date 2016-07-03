from flask import Flask
from app import config

app = Flask('Image classification backend', static_url_path="", static_folder=config.STATIC_FOLDER_PATH)

from app.mod_root import mod_root as root_module
from app.mod_collections import mod_collections as collections_module
from app.mod_models import mod_models as models_module

app.register_blueprint(root_module)
app.register_blueprint(collections_module)
app.register_blueprint(models_module)
