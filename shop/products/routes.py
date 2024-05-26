from flask import render_template,redirect,url_for,flash,request
from shop import app,db
from .models import Brand,Category,Addproduct
from .forms import AddProductForm 
from werkzeug.utils import secure_filename
import os
import uuid
from shop._global import checkuser

app.config['UPLOAD_FOLDER'] = os.path.abspath('shop/static/uploads')

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
        image_1 = request.files['image_1']
        image_2 = form.image_2.data
        image_3 = form.image_3.data
        brand = request.form.get('brand')
        category = request.form.get('category')

        filename_1=""
        filename_2=""
        filename_3=""
        if image_1:
            filename_1 = str(uuid.uuid1())+secure_filename(image_1.filename)
            image_1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_1))

        if image_2:
            filename_2 = str(uuid.uuid1())+secure_filename(image_2.filename)
            image_2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_2))

        if image_3:
            filename_3 = str(uuid.uuid1())+secure_filename(image_3.filename)
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

@app.route('/editproduct/<int:id>')
def editproduct(id):
    if checkuser():
        form=AddProductForm(request.form)
        brands=Brand.query.all()
        categories=Category.query.all()
        product=Addproduct.query.get(id)
    
        if request.method == 'POST':
            product.name=form.name.data
            product.price=form.price.data
            product.discount=form.discount.data
            product.stock=form.stock.data
            product.colors=form.colors.data
            product.desc = form.description.data
            image_1 = request.files['image_1']
            image_2 = form.image_2.data
            image_3 = form.image_3.data
            product.brand = request.form.get('brand')
            product.category = request.form.get('category')
    
            filename_1=""
            filename_2=""
            filename_3=""
            if image_1:
                filename_1 = str(uuid.uuid1())+secure_filename(image_1.filename)
                image_1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_1))
                product.image_1=filename_1
    
            if image_2:
                filename_2 = str(uuid.uuid1())+secure_filename(image_2.filename)
                image_2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_2))
                product.image_2=filename_2

            if image_3:
                filename_3 = str(uuid.uuid1())+secure_filename(image_3.filename)
                image_3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_3))
                product.image_3=filename_3

            db.session.commit()
            flash(f'The product has been added to your database','success')
            return redirect(url_for('home'))
        return render_template('products/editproduct.html',form=form,title="Edit Product",product=product,brands=brands,categories=categories)
        
    