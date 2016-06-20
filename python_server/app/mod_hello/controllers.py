from flask import Blueprint, request, redirect

mod_hello = Blueprint('hello', __name__, url_prefix='/hello')


@mod_hello.route('/')
def hello():
    return 'Hello, world!'
