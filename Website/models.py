from . import db


productdetails = db.Table('productdetails',
db.Column('product_id', db.Integer, db.ForeignKey('products.id'), nullable=False),
db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), nullable=False),
db.PrimaryKeyConstraint('product_id','cart_id'))


class Products(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(30), nullable=False, default = 'tshirt.jpg')
    category = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer)
    sale = db.Column(db.String(3), nullable=False)
    size = db.Column(db.String(5), nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Price: {}, Image: {}, Category: {}, Stock: {}, Sale: {}, size: {}, Qty: {} \n" 
        str =str.format( self.id, self.name, self.description, self.price, self.image, self.category, self.stock, self.sale, self.size, self.qty)
        return str

class Enquiry(db.Model):
    __tablename__='enquiry'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer)
    message = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        str = "Id: {}, First Name: {}, Last Name: {}, Email: {}, Phone: {}, Message: {}\n" 
        str =str.format( self.id, self.firstname,self.lastname,self.email, self.phone, self.message)
        return str

class Cart(db.Model):
    __tablename__="cart"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer)
    products = db.relationship("Products", secondary = productdetails, backref="cart")
    no_of_items = db.Column(db.Integer)
    total_cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        str = "id: {}, Status: {}, Firstname: {}, Lastname: {}, Email: {}, Phone: {}, Products: {}, No of Items: {}, Total Cost: {}\n" 
        str =str.format( self.id, self.status,self.firstname,self.lastname,
        self.email, self.phone, self.products, self.no_of_items, self.total_cost)
        return str

