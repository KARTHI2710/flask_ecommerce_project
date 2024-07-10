from shop import db,app
from datetime import datetime

class Register(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), primary_key=False)
    username=db.Column(db.String(50),unique=True)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(50),unique=False)
    country=db.Column(db.String(50),unique=False)
    state=db.Column(db.String(50),unique=False)
    city=db.Column(db.String(50),unique=False)
    contact=db.Column(db.String(50),unique=False)
    address=db.Column(db.String(50),unique=False)
    zipcode=db.Column(db.String(50),unique=False)
    profile=db.Column(db.String(200),unique=False,default='profile.jpg')
    date_created = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return '<Register %r>'% self.name
    
with app.app_context():
    db.create_all()