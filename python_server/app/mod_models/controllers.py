from flask import Blueprint, request, redirect, jsonify, send_file, abort
from imclas.data_acquisition import DAL
from imclas.classifiers import SVMClassifierBuilder
import os

mod_models = Blueprint('models', __name__, url_prefix='/api/models')


def convert_classifier_db_model_to_item(obj):
    id = obj[0]
    name = obj[1]
    path = obj[2]
    return {'path': path,
            'id': id,
            'name': name}


@mod_models.route('/', methods=['GET', 'POST'])
def get_models():
    d = DAL()
    if request.method == 'GET':
        classifiers = d.get_all_classifiers('svm')
        return jsonify(classifiers=map(convert_classifier_db_model_to_item, list(classifiers)))
    elif request.method == 'POST':
        svm_builder = SVMClassifierBuilder()
        model_object = request.json

        result = svm_builder.build_model(collections=model_object['collections'],
                                         number_of_clusters=model_object['clusters'],
                                         train_percentage=float(model_object['trainPercentage']),
                                         svm_type=model_object['type'])

        return jsonify(result=result)


@mod_models.route('/<name>', methods=['DELETE'])
def delete_model(name):
    d = DAL()
    try:
        d.remove_classifier(name, 'kmeans')
        d.remove_classifier(name, 'svm')
        return jsonify({'message': 'ok'})
    except Exception as e:
        return jsonify({'error': e})
