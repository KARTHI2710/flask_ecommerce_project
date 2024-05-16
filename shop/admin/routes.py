from flask import render_template,redirect,url_for,request,session,flash
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User

@app.route('/')
def home():
    return render_template('admin/index.html',title="Home")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password=bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.name.data, 
            username=form.username.data,
            email=form.email.data,
            password=hash_password,
            # profile=form.profile.data
            )
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}',"success")
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form , title="Registration form")

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm(request.form)
    if request.method=='POST' and form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            session['email']=form.email.data
            flash(f'Hello {form.email.data}','success')
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash(f"Invalid password",'danger')
            return redirect(url_for('login'))
        

    return render_template('admin/login.html',form=form,title='Login Page')
