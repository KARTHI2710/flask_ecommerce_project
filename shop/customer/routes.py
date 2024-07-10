from flask import render_template,redirect,url_for,flash,request
from shop import app,db,search,bcrypt
from .forms import CustomerRegisterForm
from .models import Register

@app.route('/customer/register',methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
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