from flask import render_template,redirect,url_for,flash,request
from shop import app,db
from .models import Brand,Category

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