from flask import Flask, render_template, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app=Flask(__name__)

def create_app():
    
    app.debug=True
    app.secret_key='ecommercewebsite1234'

    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bazinga.sqlite'
    
    db.init_app(app)
    bootstrap = Bootstrap(app)
    from . import views
    app.register_blueprint(views.bp)
    return app
    
@app.errorhandler(404) 

def not_found(e): 
  return render_template("404.html")

@app.errorhandler(500)
def internal_error(e):
  return render_template("500.html")

