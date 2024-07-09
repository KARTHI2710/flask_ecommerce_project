from flask import render_template,redirect,url_for,flash,request
from shop import app,db,search
from .forms import CustomerRegisterForm

@app.route('/customer/register',methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    return render_template('customer/register.html',form=form)