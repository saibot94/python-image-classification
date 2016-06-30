from flask import Blueprint, request, redirect, jsonify, abort
from werkzeug.utils import secure_filename
from imclas.data_acquisition import DAL
from imclas.features import FeatureExtractor
from app import config

from imclas.classifiers import SVMClassifierBuilder
import os

mod_models = Blueprint('models', __name__, url_prefix='/api/models')
ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif', 'jpeg'}


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
                                         svm_type=model_object['type'],
                                         limit=model_object['limit'])

        return jsonify(result=result)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@mod_models.route('/<name>', methods=['DELETE'])
def delete_model(name):
    d = DAL()
    try:
        d.remove_classifier(name, 'kmeans')
        d.remove_classifier(name, 'svm')
        return jsonify({'message': 'ok'})
    except Exception as e:
        return jsonify({'error': e})


def get_svm_probability_result(svm_classifier, item):
    probability = None
    if svm_classifier.probability:
        probability_percentages = svm_classifier.predict_proba([item])
        probability = zip(svm_classifier.classes_.tolist(), probability_percentages.tolist()[0])
        probability = sorted(probability, key=lambda x: x[1], reverse=True)
    return probability


def classify_image_path(model_name, image_path):
    try:
        d = DAL()
        kmeans_classifier = d.load_classifier_object(model_name, 'kmeans')
        svm_classifier = d.load_classifier_object(model_name, 'svm')
        if kmeans_classifier is not None and svm_classifier is not None:
            feature_extractor = FeatureExtractor()
            image_histograms = feature_extractor.extract_histograms_from_images(kmeans_classifier, [image_path])
            prediction = svm_classifier.predict([image_histograms[0]])
            print 'classified: {}'.format(str(prediction))

            prediction_result = {'class': prediction.tolist()[0],
                                 'probability': get_svm_probability_result(svm_classifier, image_histograms[0])
                                 }
            return prediction_result
        else:
            abort(404)
    except Exception as e:
        print '[ERROR] : {}'.format(e)
        abort(500)
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)


@mod_models.route('/classify/<model_name>', methods=['POST'])
def upload_image_for_classification(model_name):
    if 'file' not in request.files:
        abort(400)
    posted_image = request.files['file']
    if posted_image and allowed_file(posted_image.filename):
        filename = secure_filename(posted_image.filename)
        image_path = os.path.join(config.UPLOAD_PHOTO_PATH, filename)
        posted_image.save(image_path)
        if os.path.exists(image_path):
            classification_result = classify_image_path(model_name, image_path)
            print '[LOG] Classification result: {}'.format(str(classification_result))
            return jsonify(prediction=classification_result)
        else:
            abort(400)
