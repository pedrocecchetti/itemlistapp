from models import Base, User, Category, Item, engine
from flask import Flask, jsonify, request, url_for, abort, g, render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from  sqlalchemy.sql.expression import func, select
import random

from flask_httpauth import HTTPBasicAuth
import json

#NEW IMPORTS
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests
from google.oauth2 import id_token
from google.auth.transport import requests

Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
app = Flask(__name__)
session = Session()


CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']


@app.route('/login')
def start():
    return render_template('clientOAuth.html')



@app.route('/')
def render_landing_page():
    # When you get to this route, it shows the index page with some items and 
    # a sidebar menu to navigate through the categories
    # First we need to store 5 first items
    five_random_item = []
    # for i in range(1,6):
    #     item_list.append(session.query(Item).filter_by(id = i).first())
    item_list = session.query(Item).all()
    item_size =  len(item_list)
    category_list = session.query(Category).all()
    for i in range(0,6):
        five_random_item.append(item_list[random.randint(0,item_size-1)])

    return render_template('landing_page.html', items = five_random_item, categorys = category_list)

@app.route('/category/<int:category_id>')
def render_category_page(category_id):
    category = session.query(Category).filter_by(id = category_id).first()
    items = session.query(Item).filter_by(category_id = category_id).all()
    first_items = items[0:5]
    return render_template('category_page.html', category = category, items = first_items)

@app.route('/category/<int:category_id>/item/<int:item_id>')
def render_item_page(category_id,item_id):
    category = session.query(Category).filter_by(id = category_id).first()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('item_page.html', category = category, item= item)

@app.route('/category/<int:category_id>/item/new')
def render_add_new_item_page(category_id):
    category = session.query(Category).filter_by(id = category_id).first()
    return render_template('add_new_item_page.html', category = category)

@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def edit_item(item_id, category_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('edit_item.html', item = item)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def delete_item(item_id, category_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('delete_item.html', item = item)


if __name__ == '__main__':
    app.debug = True
    #app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
