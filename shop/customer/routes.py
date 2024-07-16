from flask import render_template,redirect,url_for,flash,request
from shop import app,db,search,bcrypt,login_manager
from .forms import CustomerRegisterForm,CustomerLoginForm
from .models import Register
from flask_login import login_required,current_user,logout_user,login_user

@app.route('/customer/register',methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm(request.form)
    print(form.errors)
    if form.validate_on_submit():
        hash_password=bcrypt.generate_password_hash(form.password.data)

        register_obj=Register(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            address=form.address.data,
            zipcode=form.zipcode.data
        )
        db.session.add(register_obj)
        flash(f'Welcom {form.name.data} Thank you for registering','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html',form=form)


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user)
           flash('You are login now!', 'success')
           return redirect(url_for('homeproduct'))
        flash('incorrect email and password','danger')
        return redirect(url_for('customerLogin'))
    
    return render_template('customer/login.html',form=form)

@app.route('/customer/logout' , methods=['GET','POST'])
def customer_logout():
    logout_user()
    return redirect(url_for('customerLogin'))

