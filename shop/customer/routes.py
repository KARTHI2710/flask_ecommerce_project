from flask import render_template,redirect,url_for,flash,request,session
from shop import app,db,search,bcrypt,login_manager
from .forms import CustomerRegisterForm,CustomerLoginForm
from .models import Register,CustomerOrder
from flask_login import login_required,current_user,logout_user,login_user
import secrets

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

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        print(current_user)
        customer_id=current_user.id 
        invoice=secrets.token_hex(5)
        print(customer_id)
        print(invoice)
        try:
            order=CustomerOrder(
                invoice=invoice,
                customer_id=customer_id,
                orders=session['Shoppingcart']
            )
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent','success')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order','danger')
            return redirect(url_for('displaycart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandtotal=0
        subtotal=0
        customer_id =current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(invoice=invoice).first()
        for key,product in orders.orders.items():
                discount=(product['discount']/100)*float(product['price'])
                subtotal+=int(product['quantity'])*(float(product['price'])-discount)
                grandtotal+=float(product['price'])*int(product['quantity']) 
    else:
        return redirect(url_for('customerLogin'))
    
    return render_template('customer/orders.html',invoice=invoice,subtotal=subtotal,grandtotal=grandtotal,customer=customer,
                           orders=orders)
