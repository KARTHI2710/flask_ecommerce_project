from flask_wtf.file import FileAllowed,FileField,FileRequired
from wtforms import Form,IntegerField,StringField,TextAreaField,BooleanField,validators

class AddProductForm(Form):
    name=StringField('Name',[validators.DataRequired()])
    price=IntegerField('Price',[validators.DataRequired()])
    discount=IntegerField('Discount',default=0)
    stock=IntegerField('Stock',[validators.DataRequired()])
    description=TextAreaField('Description',[validators.DataRequired()])
    colors=TextAreaField('Colors',[validators.DataRequired()])

    image_1 = FileField('Image_1',validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'],'Images only')
    ])
    image_2 = FileField('Image_2', validators=[
        
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only')
    ])
    image_3 = FileField('Image_3', validators=[
        
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only')
    ])