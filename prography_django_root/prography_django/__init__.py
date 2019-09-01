import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('prography-django-firebase-adminsdk-uff6l-40efdc538f.json')
firebase_admin.initialize_app(cred)



#post_number=0