from contact_keeper import db

# Define models
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    addresses = db.relationship('Address', backref='owner', lazy=True, order_by='desc(Address.is_primary)')
    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_1 = db.Column(db.String(100), nullable=False)
    street_2 = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)