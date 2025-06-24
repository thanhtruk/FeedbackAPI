from datetime import datetime
from API.firebase_config import db


def generate_custom_id(collection_name: str) -> str:
    counter_ref = db.collection("counters").document(collection_name)
    counter_doc = counter_ref.get()

    if counter_doc.exists:
        count = counter_doc.to_dict().get("count", 0) + 1
    else:
        count = 1

    counter_ref.set({"count": count})  # update counter

    today = datetime.today()
    date_part = today.strftime("%m-%d")

    custom_id = f"{collection_name[0]}{count}-{date_part}"
    return custom_id
