from flask import Flask, render_template, Blueprint, request, session, flash, redirect, url_for
from .models import Products, Enquiry, Cart
from . import db
from .forms import CheckoutForm

app = Flask(__name__)

bp = Blueprint('main', __name__)

# --------------------------------------Data-----------------------------#

bp = Blueprint('main',__name__)


@bp.route("/")
def home():
    products = Products.query.filter(Products.id<10).all()
    return render_template('home.html', products = products)

@bp.route("/for-sale-products")
def sale():
    forsale = Products.query.filter(Products.sale == 'yes').all()
    return render_template('filterproducts.html', products = forsale, category = "FOR SALE") 



@bp.route('/searched-products/')
def search():
	search = request.args.get('search')
	search = '%{}%'.format(search) # substrings will match
	product = Products.query.filter(Products.description.like(search)).all()
	return render_template('filterproducts.html', products = product, category = 'Search Results')
    


#----------------------------------------------------------SORTING------------------------------------------------------#

@bp.route('/products/<category>', methods = ['POST','GET'])
def sort(category):
    allproducts = Products.query.filter(Products.category == category)
    if request.method == 'POST':
        price = request.values.get('filter')
        sale = request.values.get('sale')
        
        if price == 'priceinc' and sale is None:
            sortedinc = Products.query.filter(Products.category == category).order_by(Products.price)
            return render_template('products.html', items = sortedinc, category = category)
        elif price == 'pricedesc' and sale is None:
            sorteddesc = Products.query.filter(Products.category == category).order_by(Products.price.desc())
            return render_template('products.html', items = sorteddesc, category = category)
        elif sale == 'sale' and price == 'priceinc':
            #if price == 'priceinc':
            inc = Products.query.filter(Products.sale.contains('yes'), Products.category == category)
            sale = inc.order_by(Products.price)
            return render_template('products.html', items = sale, category = category)
        elif sale == 'sale' and price == 'pricedesc':
            desc = Products.query.filter(Products.sale.contains('yes'), Products.category == category)
            sale = desc.order_by(Products.price.desc())
            return render_template('products.html', items = sale, category = category)
        elif sale =='sale':
            psale = Products.query.filter(Products.sale.contains('yes'), Products.category == category)
            return render_template('products.html',items = psale, category = category)
    return render_template('products.html',items = allproducts, category = category)


#----------------------------------------CONTACT--------------------------------------------------#

@bp.route("/contact", methods = ['GET','POST'])
def contact():
    enq = None
    if enq is None:
        enq = Enquiry(firstname = '', lastname = '', email = '', phone = 0, message = '')
    try:
        print(str(enq))
        db.session.add(enq)
        db.session.commit()
    except:
        print('Failed to create the enquiry')

    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        print('The entered details are:\nfirstname: {}\nlastname: {}\nemail: {}\nphone: {}\nmessage: {}'.format(firstname,lastname,email,phone,message))
        enq = Enquiry(firstname = firstname, lastname = lastname, email = email, phone = phone, message = message)
        try:
            db.session.add(enq)
            db.session.commit()
        except:
            print('Failed to save the enquiry')
        return render_template('enquirydone.html', fname = firstname, lname = lastname, email = email, phone = phone, message = message)
    else:
        return render_template('contact.html' )


#----------------------------------------PRODUCTS--------------------------------------------------#

@bp.route("/products/<category>")
def products(category):
    allproducts = Products.query.filter(Products.category == category)
    return render_template('products.html', items = allproducts, category = category)


#----------------------------------------PRODUCTS DETAILS--------------------------------------------------#

@bp.route("/products/<int:pid>/<pcat>/<pname>/<pimg>/<pprice>")
def details(pid,pname,pcat,pimg,pprice):
    return render_template('productdetails.html',pid = pid, pname = pname, pcat = pcat, pimg = pimg, pprice = pprice)


#----------------------------------------SHOPPING CART--------------------------------------------------#

@bp.route("/shoppingcart", methods = ['POST','GET'])
def addtocart():

    product_id = request.values.get('product_id')  
    size = request.values.get('options')
    qty = request.values.get('qty')
  
    # retrieve products in cart 
    if 'cart_id' in session.keys():
        cart = Cart.query.get(session['cart_id'])

    else: # The cart is empty
        cart = None

    # Create a shopping cart for products
    if cart is None:
        cart = Cart(status = False, firstname = '',lastname = '',email = '', phone = '', no_of_items = 0, total_cost = 0)
        try:
            db.session.add(cart)
            db.session.commit()
            session['cart_id'] =  cart.id
        except:
            print('failed to create a shopping cart')
            cart = None

    
# calculating total price
    totalprice = 0
    if cart is not None:
        for product in cart.products:
            totalprice = totalprice + (product.price * product.qty)

# calculating total items
    totalitems = 0
    if cart is not None:
        for product in cart.products:
            totalitems += 1

# Shipping charges
    shipping = 0
    if totalitems != 0:
        shipping = 10


   
 # adding a product     
    if product_id is not None and cart is not None:
        product = Products.query.get(product_id) 
        
        if product not in cart.products:   
            
            try:
                product.qty = qty
                Products.stock = Products.stock - qty
                product.size = size
                cart.products.append(product)
                db.session.add(cart)
                db.session.commit()
                
                    
            except:
                return 'There was some issue adding the product in the basket'
            return redirect(url_for('main.addtocart'))    

        else:
            flash('The product is already in the basket')
            return redirect(url_for('main.addtocart'))
    return render_template('cart.html', cart = cart, totalprice = totalprice, totalitems = totalitems, shipping = shipping)
         


#------------------------------------------Empty the Cart-----------------------------------------------------#

@bp.route("/emptycart")
def emptycart():
    if 'cart_id' in session:
        del session['cart_id']
        flash('All items deleted.')
    return redirect(url_for('main.home'))    


#---------------------------------------Remove an item from cart-----------------------------------------------#

@bp.route("/deleteditem/", methods =['POST'])
def deleteitem():
    id = request.form.get('id')
    if 'cart_id' in session:
        cart = Cart.query.get_or_404(session['cart_id'])
     
        deleteproduct = Products.query.get(id)
        print(deleteproduct)
        try:
            cart.products.remove(deleteproduct)
            db.session.commit()
            return redirect(url_for('main.addtocart'))
        except:
            return 'Problem deleting the item from Cart'
    return redirect(url_for('main.addtocart'))



#------------------------------------------------Checkout Form-------------------------------------------------------#

@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    form = CheckoutForm() 
    if 'cart_id' in session:
        cart = Cart.query.get_or_404(session['cart_id'])
       
        if form.validate_on_submit():
            cart.status = True
            cart.firstname = form.firstname.data
            cart.lastname = form.lastname.data
            cart.email = form.email.data
            cart.phone = form.phone.data
            cart.address = form.address.data
            totalcost = 0
            for product in cart.products:
                totalcost = totalcost + product.price
            cart.totalcost = totalcost
            try:
                db.session.add(cart)
                db.session.commit()
                del session['cart_id']
                flash('Order Placed! Thank you for placing your order.')
                return redirect(url_for('main.home'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form = form)



  