from flask import request

from API.firebase_config import db
from API.utils.generate_id import generate_custom_id
from datetime import datetime

collection_name = "feedback"
def get_all_feedback():
    limit = int(request.args.get('limit', 100))
    start_after_id = request.args.get('start_after_id')

    col_ref = db.collection(collection_name).order_by('__name__')

    if start_after_id:
        start_after_doc = db.collection(collection_name).document(start_after_id).get()
        if start_after_doc.exists:
            col_ref = col_ref.start_after(start_after_doc)

    docs = col_ref.limit(limit).stream()
    feedbacks = [doc.to_dict() | {"id": doc.id} for doc in docs]
    return feedbacks

def get_feedback_by_id(feedback_id):
    doc_ref = db.collection(collection_name).document(feedback_id)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        data['id'] = doc.id
        return data
    return None


def create_feedback(data):
    required_fields = [
        "title", "field", "field_detail", "content",
        "clauses_sentiment", "status", "response"
    ]

    data["create_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    new_id = generate_custom_id(collection_name)

    db.collection(collection_name).document(new_id).set(data)

    return new_id


def update_feedback(feedback_id, data):
    if not feedback_id:
        raise ValueError("Feedback ID is required for update.")

    if not data or not isinstance(data, dict):
        raise ValueError("Update data must be a non-empty dictionary.")

    allowed_fields = {
        "field", "clauses_sentiment", "status", "response"
    }
    invalid_fields = [key for key in data if key not in allowed_fields]
    if invalid_fields:
        raise ValueError(f"Invalid fields in update: {', '.join(invalid_fields)}")

    doc_ref = db.collection(collection_name).document(feedback_id)
    if not doc_ref.get().exists:
        raise ValueError(f"Feedback with ID '{feedback_id}' does not exist.")

    doc_ref.update(data)


def delete_feedback(feedback_id):
    db.collection(collection_name).document(feedback_id).delete()
