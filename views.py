from models import Base, User, Category, Item, engine
from flask import Flask, jsonify, request, url_for, render_template, flash
from flask import redirect, g, abort
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func, select

import random
import requests

from flask_httpauth import HTTPBasicAuth
from flask import json

Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
app = Flask(__name__)
app.secret_key = "BYUGSDI&907897778dgbas87ybYUDFSJJIsfbydugfy7".encode('utf8')
session = Session()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']


@app.route('/googleauth', methods=['POST'])
def start():
    # Get the content on the POST request
    response = request.get_json()
    username = response['username']
    image_url = response['image_url']
    id_token = response['id_token']
    # Token Validation
    auth_response = requests.get(
                    '''https://oauth2.googleapis.com/tokeninfo?
                    id_token={}'''.format(id_token))

    if auth_response.status_code == 200:
        # If response is 200
        # import google sub from response
        google_sub = json.loads(auth_response.text)['sub']
        # Create the session
        login_session['username'] = username
        login_session['image_url'] = image_url
        login_session['id_token'] = id_token
        login_session['google_sub'] = google_sub
        # Pull user from DB
        user = session.query(User).filter_by(google_sub=google_sub).first()
        # if user in DB just log and update id_token
        if user:
            user.id_token = id_token
            session.add(user)
            session.commit()
            print("Successfully Logged In!")
        else:
            # If the user is not in DB create a new user
            new_user = User(username=username, google_sub=google_sub,
                            id_token=id_token, image_url=image_url)
            session.add(new_user)
            session.commit()
            print("Successfully Logged In!")
    else:
        abort(404)

    return redirect(url_for('render_landing_page'), code=200)


@app.route('/')
def render_landing_page():
    # When you get to this route, it shows the index page with some items and
    # a sidebar menu to navigate through the categories
    # Storing 5 random items
    five_random_item = []
    item_list = session.query(Item).all()
    item_size = len(item_list)
    category_list = session.query(Category).all()
    for i in range(0, 6):
        five_random_item.append(item_list[random.randint(0, item_size-1)])
    # Conditional for Login/Logout buttons
    log = ''
    if 'username' in login_session:
        log = True

    return render_template('landing_page.html', items=five_random_item,
                           categorys=category_list, log=log)


@app.route('/category/<int:category_id>')
def render_category_page(category_id):
    log = ''
    # Conditional for Login/Logout buttons
    if 'username' in login_session:
        log = True

    # Pull Category and Items from DB
    category = session.query(Category).filter_by(id=category_id).first()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('category_page.html', category=category,
                           items=items, log=log)


@app.route('/category/<int:category_id>/item/<int:item_id>')
def render_item_page(category_id, item_id):
    log = ''
    # Conditional for Login/Logout buttons
    if 'username' in login_session:
        log = True

    # Pull Category and Item from DB
    category = session.query(Category).filter_by(id=category_id).first()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item_page.html',
                           category=category, item=item, log=log)


@app.route('/category/<int:category_id>/item/new', methods=['GET', 'POST'])
def render_add_new_item_page(category_id):
    # Pull the Category from DB to use as an object
    category = session.query(Category).filter_by(id=category_id).first()

    # Route for the POST methos
    if request.method == 'POST':
        # Pull User from DB and store google_sub
        user = session.query(User).filter_by(
               google_sub=login_session['google_sub']).first()
        user_id = user.id
        # Create new item
        new_item = Item(item_name=request.form['item_name'],
                        item_description=request.form['item_name'],
                        category_id=category_id, user_id=user_id)
        session.add(new_item)
        session.commit()
        print('Item added!')
        flash('Item Added!')
        return redirect(url_for('render_category_page',
                                category_id=category.id), code=302)
    else:
        # For GET route
        log = ''
        # Conditional for Login/Logout buttons
        if 'username' not in login_session:
            flash("You're Not Logged in, please Log in!")
            return redirect(url_for('render_category_page',
                                    category_id=category.id), code=302)
        else:
            log = True

        return render_template('add_new_item_page.html',
                               category=category, log=log)


@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def edit_item(item_id, category_id):
    item = session.query(Item).filter_by(id=item_id).first()
    if request.method == 'POST':
        item.item_name = request.form['item_name']
        item.item_description = request.form['item_description']
        session.add(item)
        session.commit()
        flash('Item successfully edited!')
        return redirect(url_for('render_category_page',
                                category_id=item.category_id))
    else:
        item_user_sub = item.user.google_sub
        log = ''
        # Conditional for Login/Logout buttons
        if 'username' not in login_session:
            flash("You're Not Logged in, please Log in!")
            return redirect(url_for('render_item_page',
                            category_id=category_id,
                            item_id=item_id), code=302)
        # Conditional for Item Ownership
        elif login_session['google_sub'] != item_user_sub:
            flash('You cannot edit this item, because you are not owner!')
            log = False
            return redirect(url_for('render_item_page',
                            category_id=category_id,
                            item_id=item_id), code=302)
        # If User passes everything then Render Edit Template
        else:
            log = True
            return render_template('edit_item.html', item=item, log=log)


@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def delete_item(item_id, category_id):
    item = session.query(Item).filter_by(id=item_id).first()
    item_user_sub = item.user.google_sub
    if request.method == 'POST':
        session.delete(item)
        session.commit()
    else:
        # Conditional for Login/Logout buttons
        if 'username' not in login_session:
            flash("You're Not Logged in, please Log in!")
            return redirect(url_for('render_item_page',
                            category_id=category_id,
                            item_id=item_id), code=302)
        # Conditional for Item Ownership
        elif login_session['google_sub'] != item_user_sub:
            flash('You cannot delete this item, because you are not owner!')
            log = False
            return redirect(url_for('render_item_page',
                            category_id=category_id,
                            item_id=item_id), code=302)
        # If User passes everything then Render Edit Template
        else:
            log = True
            return render_template('edit_item.html', item=item, log=log)
        log = ''
        item = session.query(Item).filter_by(id=item_id).one()
        return render_template('delete_item_page.html', item=item, log=log)


@app.route('/logout', methods=['POST'])
def logout():
    login_session.pop('username', None)
    login_session.pop('image_url', None)
    login_session.pop('id_token', None)
    print(login_session)
    return redirect(url_for('render_landing_page'), code=302)


@app.route('/allitems/JSON')
def get_json_items():
    items = session.query(Item).all()
    print(dict(items[0]))   



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
