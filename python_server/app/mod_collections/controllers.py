from flask import Blueprint, request, redirect, jsonify, send_file, abort
from imclas.data_acquisition import DAL
from imclas.collections import CollectionManager
import os
import thread, time
from threading import Thread

mod_collections = Blueprint('collections', __name__, url_prefix='/api/collections')


def get_collection_obj(collection, dal):
    collection_obj = {'id': collection[0], 'name': collection[1]}
    collection_obj['items'] = dal.get_items_in_collection(collection_obj['name'])
    return collection_obj


@mod_collections.route('/')
def get_collections():
    d = DAL()
    collections = d.get_collections()
    collections_result = []
    for collection in collections:
        collection_obj = get_collection_obj(collection, d)
        collections_result.append(collection_obj)
    return jsonify(result=collections_result)


@mod_collections.route('/<collection_name>', methods=['GET', 'DELETE'])
def get_or_delete_collection_with_name(collection_name):
    if request.method == 'GET':
        return get_collection_with_name(collection_name)
    elif request.method == 'DELETE':
        return delete_collection_with_name(collection_name)


@mod_collections.route('/<collection_name>/<query>/<number_of_items>', methods=['POST'])
def create_collection_with_name(collection_name, query, number_of_items):
    print "[LOG] Getting collection: {}, {}, {}".format(collection_name, query, number_of_items)

    collection_manager = CollectionManager()
    print collection_manager.create_collection(query,
                                               int(number_of_items),
                                               collection_name)

    return jsonify({'message': 'created'})


def get_collection_with_name(collection_name):
    d = DAL()
    collections = d.get_collections()
    filtered_collection = filter(lambda c: c[1] == collection_name, collections)
    if len(filtered_collection) > 0:
        return jsonify(result=get_collection_obj(filtered_collection[0], d))
    else:
        abort(404)


def delete_collection_with_name(collection_name):
    collection_manager = CollectionManager()
    try:
        collection_manager.remove_collection(collection_name)
        return jsonify(result={'message': 'ok'})
    except Exception as e:
        print e
        abort(404)


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
