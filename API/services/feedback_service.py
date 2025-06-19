from API.firebase_config import db
from API.utils.generate_id import generate_custom_id

collection_name = "feedback"
def get_all_feedback():
    feedbacks = db.collection(collection_name).stream()
    return [fb.to_dict() | {"id": fb.id} for fb in feedbacks]

def get_feedback_by_id(feedback_id):
    doc = db.collection(collection_name).document(feedback_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_feedback(data):
    new_id = generate_custom_id(collection_name)
    doc_ref = db.collection(collection_name).document(new_id).set(data)
    return new_id

def update_feedback(feedback_id, data):
    db.collection(collection_name).document(feedback_id).update(data)

def delete_feedback(feedback_id):
    db.collection(collection_name).document(feedback_id).delete()
