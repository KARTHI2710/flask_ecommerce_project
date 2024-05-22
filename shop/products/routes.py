from flask import render_template,redirect,url_for,flash,request
from shop import app,db
from .models import Brand,Category,Addproduct
from .forms import AddProductForm 

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
        desc = form.desc.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        # image_1 =
        # image_2 =
        # image_3 = 

        addpro=Addproduct(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            colors=colors,
            desc=desc,
            brand_id=brand,
            category_id=category
        )
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database','success')
        return redirect(url_for('home'))
    return render_template('products/addproduct.html',form=form,title="Add Product",brands=brands,categories=categories)