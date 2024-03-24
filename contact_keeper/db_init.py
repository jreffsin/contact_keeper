from contact_keeper import application, db
from contact_keeper.models import Contact, Address
from sqlalchemy.exc import DatabaseError

try:
    with application.app_context():
        db.create_all()
except DatabaseError as err:
    if 'already exists' in err._sql_message():
        print("Databases already exist.")
    else:
        print(err)