import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Initialize Firebase
    cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    # Test connection
    test_doc = db.collection('test').document('test')
    test_doc.set({'test': 'test'})
    test_doc.delete()
    
    print("✅ Firebase подключение работает корректно")
except Exception as e:
    print("❌ Ошибка Firebase:", str(e)) 