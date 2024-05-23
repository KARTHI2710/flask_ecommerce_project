from flask import render_template,redirect,url_for,flash,request
from shop import app,db
from .models import Brand,Category,Addproduct
from .forms import AddProductForm 
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method=='POST':
        brandname=request.form.get('brand')
        brand=Brand(
            name=brandname
        )
        db.session.add(brand)
        flash(f"{brandname} added successfully","success")
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',title='Add Brand',brands="brand")

@app.route('/addcategory',methods=['GET','POST'])
def addcategory():
    if request.method=='POST':
        categoryname=request.form.get('category')
        cat=Category(
            name=categoryname
        )
        db.session.add(cat)
        flash(f"{categoryname} added successfully","success")
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html',title='Add Brand')

@app.route('/addproduct',methods=['GET','POST'])
def addproduct():
    form=AddProductForm(request.form)
    brands=Brand.query.all()
    categories=Category.query.all()

    if request.method == 'POST':
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stock.data
        colors=form.colors.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = form.image_1.data
        image_2 = form.image_2.data
        image_3 = form.image_3.data

        filename_1=""
        filename_2=""
        filename_3=""
        if image_1:
            filename_1 = secure_filename(image_1.filename)
            image_1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_1))

        if image_2:
            filename_2 = secure_filename(image_2.filename)
            image_2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_2))

        if image_3:
            filename_3 = secure_filename(image_3.filename)
            image_3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_3))

        addpro=Addproduct(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            colors=colors,
            desc=desc,
            brand_id=brand,
            category_id=category,
            image_1=filename_1,
            image_2=filename_2,
            image_3=filename_3
        )
        db.session.add(addpro)
        db.session.commit()
        flash(f'The product {name} has been added to your database','success')
        return redirect(url_for('home'))
    return render_template('products/addproduct.html',form=form,title="Add Product",brands=brands,categories=categories)