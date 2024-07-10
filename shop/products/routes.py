from flask import render_template,redirect,url_for,flash,request
from shop import app,db,search
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
        return redirect(url_for('addcategory'))
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

@app.route('/editproduct/<int:id>',methods=['GET','POST'])
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
            
            product.brand_id = request.form.get('brand')
            product.category_id = request.form.get('category')
    
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
        
@app.route('/deleteproduct/<int:id>',methods=['GET','POST'])
def deleteproduct(id):
    if checkuser():
        product=Addproduct.query.get(id)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('showcategories'))
    


    
@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if checkuser():
        update_brand=Brand.query.get_or_404(id)
        if request.method=='POST':
            brand=request.form.get('brand')
            update_brand.name=brand
            flash('Your Brand has been updated','success')
            db.session.commit()
            return redirect(url_for('showbrands'))
        return render_template('products/updatebrand.html',title='Update brand page',brand=update_brand)


@app.route('/deletebrand/<int:id>',methods=['GET','POST'])
def deletebrand(id):
    if checkuser():
        brand=Brand.query.get_or_404(id)
        db.session.delete(brand)
        db.session.commit()
        return redirect(url_for('showbrands'))
    
@app.route('/deletecategory/<int:id>',methods=['GET','POST'])
def deletecategory(id):
    if checkuser():
        category=Category.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('showcategories'))
    
    
@app.route('/updatecategory/<int:id>',methods=['GET','POST'])
def updatecategory(id):
    if checkuser():
        update_category=Category.query.get_or_404(id)
        if request.method=='POST':
            category=request.form.get('category')
            update_category.name=category
            flash('Your Category has been updated','success')
            db.session.commit()
            return redirect(url_for('showcategories'))
        return render_template('products/updatebrand.html',title='Update brand page',category=update_category)

@app.route('/')
def homeproduct():
    page=request.args.get('page',1,type=int)
    products = Addproduct.query.paginate(page=page,per_page=1)
    #print(products)
    # print(products.items)
    # print(products.iter_pages())

    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    categories_name = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html',title="Home",products=products,brands=brands,categories=categories_name,product_paginate=True)


@app.route('/result')
def result():
    searchword=request.args.get('q')
    products=Addproduct.query.msearch(searchword,fields=['name','desc'],limit=3)

    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    categories_name = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/result.html',products=products,brands=brands,categories=categories_name)


@app.route('/brandproducts/<int:id>',methods=['GET','POST'])
def brandproduct(id):
    page=request.args.get('page',1,type=int)
    brand_id=Brand.query.filter_by(id=id).first()
    products = Addproduct.query.filter_by(brand_id=id).paginate(page=page,per_page=1)
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    categories_name = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html',title="Home",products=products,brands=brands,categories=categories_name,brand_id=brand_id)

@app.route('/categoryproducts/<int:id>',methods=['GET','POST'])
def categoryproduct(id):
    page=request.args.get('page',1,type=int)
    products = Addproduct.query.filter_by(category_id=id).paginate(page=page,per_page=1)
    brands = Brand.query.join(Addproduct,(Brand.id == Addproduct.brand_id)).all()
    categories_name = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html',title="Home",products=products,categories=categories_name,brands=brands,category_id=id)

@app.route('/singleproduct/<int:id>',methods=['GET','POST'])
def singleproduct(id):
    product = Addproduct.query.filter_by(id=id).first()
    brands=Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    return render_template('products/singleproduct.html',title="Single Product",product=product,brands=brands,categories=categories)
    