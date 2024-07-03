from flask import render_template,redirect,url_for,flash,request,session
from shop import app,db
from shop import app,db,bcrypt
from shop.products.models import Addproduct,Brand,Category
from shop._global import checkuser


def MergeDicts(dict1,dict2):
    if isinstance(dict1,list) and isinstance(dict2,list):
        return dict1+dict2
    elif isinstance(dict1,dict) and isinstance(dict2,dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart',methods=['POST'])
def AddCart():
    try:
        product_id=request.form.get('product_id')
        quantity=request.form.get('quantity')
        colors=request.form.get('colors')
        product=Addproduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method=='POST':
            DictItems = {
                product_id : {
                    'name':product.name, 'price':product.price, 'discount':product.discount, 'colors':colors,
                    'quantity':quantity,'image':product.image_1,'product_colors':product.colors
                }
            }

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart']=MergeDicts(session['Shoppingcart'],DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/cartitems',methods=['GET','POST'])
def displaycart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal=0
    grandtotal=0
    for key,product in session['Shoppingcart'].items():
        print(session['Shoppingcart'])
        discount=(product['discount']/100)*float(product['price'])
        subtotal+=float(product['price'])-discount
        grandtotal+=float(product['price']) 
    return render_template('carts/carts.html',subtotal=subtotal,grandtotal=grandtotal)
                                 
@app.route('/clearcart',methods=['GET','POST'])
def clearcart():
    try:
        session.pop('Shoppingcart')
        return redirect(url_for('home'))
    except Exception as e:
        print(e)                                 