import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("API/key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
