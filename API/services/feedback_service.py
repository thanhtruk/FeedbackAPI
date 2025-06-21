from API.firebase_config import db
from API.utils.generate_id import generate_custom_id
from datetime import datetime

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
    required_fields = [
        "title", "field", "fieldDetail",
        "clauses_sentiment", "status", "response"
    ]

    data["time"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
