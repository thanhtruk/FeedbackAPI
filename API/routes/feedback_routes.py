from flask import Blueprint, request, jsonify
from API.services.feedback_service import *

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET'])
def get_feedbacks():
    return jsonify(get_all_feedback())

@feedback_bp.route('/feedback/<feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    fb = get_feedback_by_id(feedback_id)
    return jsonify(fb or {"error": "Not found"}), 200 if fb else 404

@feedback_bp.route('/feedback', methods=['POST'])
def add_feedback():
    data = request.json
    fb_id = create_feedback(data)
    return jsonify({"id": fb_id}), 201

@feedback_bp.route('/feedback/<feedback_id>', methods=['PUT'])
def edit_feedback(feedback_id):
    update_feedback(feedback_id, request.json)
    return jsonify({"msg": "Updated"}), 200

@feedback_bp.route('/feedback/<feedback_id>', methods=['DELETE'])
def remove_feedback(feedback_id):
    delete_feedback(feedback_id)
    return jsonify({"msg": "Deleted"}), 200
