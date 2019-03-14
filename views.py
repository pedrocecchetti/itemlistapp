from models import Base, User, Category, Item, engine
from flask import Flask, jsonify, request, url_for, abort, g, render_template, flash, redirect, g
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from  sqlalchemy.sql.expression import func, select
import random

from flask_httpauth import HTTPBasicAuth
from flask import json

#NEW IMPORTS
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests
from google.oauth2 import id_token

Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
app = Flask(__name__)
app.secret_key = "Mnbishdvgaihulmfnbhvbkunlfasmnfhvyguhasilçokmlknasbufnimço".encode('utf8')
session = Session()

log = False

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']

@app.route('/googleauth', methods = ['POST'])
def start():
    # session_login['username'] = request.args[]
    username = request.get_json()['username']
    image_url = request.get_json()['image_url']
    id_token = request.get_json()['id_token']
    # Validating Token
    auth_response = requests.get('https://oauth2.googleapis.com/tokeninfo?id_token={}'.format(id_token))
    if auth_response.status_code == 200:
        print("Successfully Logged In!")
        login_session = {'username': username, 'image_url': image_url, 'id_token': id_token}
        print(login_session)
        global log 
        log = True

    return redirect(url_for('render_landing_page'), code = 302)
   




@app.route('/')
def render_landing_page():
    global log
    # When you get to this route, it shows the index page with some items and 
    # a sidebar menu to navigate through the categories
    # First we need to store 5 first items
    five_random_item = []
    print(log)
    # for i in range(1,6):
    #     item_list.append(session.query(Item).filter_by(id = i).first())
    item_list = session.query(Item).all()
    item_size =  len(item_list)
    category_list = session.query(Category).all()
    for i in range(0,6):
        five_random_item.append(item_list[random.randint(0,item_size-1)])

    return render_template('landing_page.html', items = five_random_item, categorys = category_list, log = log)

@app.route('/category/<int:category_id>')
def render_category_page(category_id):
    global log
    category = session.query(Category).filter_by(id = category_id).first()
    items = session.query(Item).filter_by(category_id = category_id).all()
    first_items = items[0:5]
    return render_template('category_page.html', category = category, items = first_items, log = log)

@app.route('/category/<int:category_id>/item/<int:item_id>')
def render_item_page(category_id,item_id):
    global log
    category = session.query(Category).filter_by(id = category_id).first()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('item_page.html', category = category, item= item, log = log)

@app.route('/category/<int:category_id>/item/new')
def render_add_new_item_page(category_id):
    global log
    category = session.query(Category).filter_by(id = category_id).first()
    return render_template('add_new_item_page.html', category = category)

@app.route('/category/<int:category_id>/item/<int:item_id>/edit')
def edit_item(item_id, category_id):
    global log
    if 'username' not in login_session:
        flash('You are not logged in')
        return redirect(url_for('render_landing_page'))
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('edit_item.html', item = item, log = log)

@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def delete_item(item_id, category_id):
    global log
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('delete_item.html', item = item, log=log)

@app.route('/logout', methods=['POST'])
def logout():
    global log
    log = False

    return redirect('/',code=302)    

if __name__ == '__main__':
    app.debug = True
    # app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
