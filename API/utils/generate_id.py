from datetime import datetime
from API.firebase_config import db


def generate_custom_id(collection_name: str) -> str:
    docs = db.collection(collection_name).get()
    count = len(docs) + 1

    today = datetime.today()
    date_part = today.strftime("%m-%d")

    custom_id = f"{collection_name[0]}{count}-{date_part}"
    return custom_id
