from flask import Blueprint, request, jsonify
from API.services.question_service import *

question_bp = Blueprint('question', __name__)

@question_bp.route('/question', methods=['GET'])
def get_feedbacks():
    return jsonify(get_all_question())

@question_bp.route('/question/<question_id>', methods=['GET'])
def get_feedback(feedback_id):
    fb = get_question_by_id(feedback_id)
    return jsonify(fb or {"error": "Not found"}), 200 if fb else 404

@question_bp.route('/question', methods=['POST'])
def add_feedback():
    data = request.json
    fb_id = create_question(data)
    return jsonify({"id": fb_id}), 201

@question_bp.route('/feedback/<feedback_id>', methods=['PUT'])
def edit_feedback(feedback_id):
    update_question(feedback_id, request.json)
    return jsonify({"msg": "Updated"}), 200

@question_bp.route('/feedback/<feedback_id>', methods=['DELETE'])
def remove_feedback(feedback_id):
    delete_question(feedback_id)
    return jsonify({"msg": "Deleted"}), 200
