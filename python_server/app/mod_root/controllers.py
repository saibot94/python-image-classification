from flask import Blueprint, request, redirect
from app import config

mod_root = Blueprint('root', __name__, url_prefix='/', static_folder=config.STATIC_FOLDER_PATH)


@mod_root.route('/')
def index():
    return mod_root.send_static_file('index.html')
