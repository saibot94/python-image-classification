from flask import Blueprint, request, redirect, jsonify, send_file
from imclas.data_acquisition import DAL
import os

mod_collections = Blueprint('collections', __name__, url_prefix='/api/collections')


@mod_collections.route('/')
def get_collections():
    d = DAL()
    collections = d.get_collections()
    collections_result = []
    for collection in collections:
        collection_obj = {'id': collection[0], 'name': collection[1]}
        collection_obj['items'] = d.get_items_in_collection(collection_obj['name'])
        collections_result.append(collection_obj)
    return jsonify(result=collections_result)


@mod_collections.route('/image', methods=['GET'])
def get_collection_image():
    name = request.args.get('name')
    if os.path.exists(name):
        return send_file(name, mimetype='image/jpeg')
    return 'Not found!'


@mod_collections.route('/image', methods=['DELETE'])
def delete_image():
    name = request.args.get('name')
    if os.path.exists(name):
        os.remove(name)
        d = DAL()
        d.remove_collection_item(name)
        return jsonify(res={'message': 'ok'})
    return jsonify(res={'message': 'not found'})
