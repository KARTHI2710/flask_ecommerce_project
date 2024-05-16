from shop import db,app

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),nullable=False,unique=True)

class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),nullable=False,unique=True)

with app.app_context():
    db.create_all()