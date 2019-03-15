from models import Base, User, Category, Item, engine
from flask import Flask, jsonify, request, url_for, abort, g, render_template, flash, redirect, g
from flask import session as login_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from  sqlalchemy.sql.expression import func, select
import random
import requests

from flask_httpauth import HTTPBasicAuth
from flask import json

Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
app = Flask(__name__)
app.secret_key = "Mnbishdvgaihulmfnbhvbkunlfasmnfhvyguhasilçokmlknasbufnimço".encode('utf8')
session = Session()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']


@app.route('/googleauth', methods = ['POST'])
def start():    

    # session_login['username'] = request.args[]
    response = request.get_json()
    username = response['username']
    image_url = response['image_url']
    id_token = response['id_token']
    # Validating Token
    auth_response = requests.get('https://oauth2.googleapis.com/tokeninfo?id_token={}'.format(id_token))
    if auth_response.status_code == 200:
        #If response is 200 Create the session
        google_sub = json.loads(auth_response.text)['sub']
        login_session['username'] = username
        login_session['image_url'] = image_url
        login_session['id_token'] = id_token
        #Pull user from DB
        user = session.query(User).filter_by(google_sub = google_sub).first()
        #if user in DB just log and update id_token
        if user:
            user.id_token = id_token
            session.add(user)
            session.commit()
            print("Successfully Logged In!")
        else:
            # If the user is not in DB create a user
            new_user = User(username = username, google_sub = google_sub, id_token = id_token,image_url = image_url)
            session.add(new_user)
            session.commit()
            print("Successfully Logged In!")
    else:
        abort(404)

    return redirect(url_for('render_landing_page'), code = 200)
   


@app.route('/')
def render_landing_page():
    # When you get to this route, it shows the index page with some items and 
    # a sidebar menu to navigate through the categories
    # Storing 5 first items
    five_random_item = []
    log = ''
    # for i in range(1,6):
    #     item_list.append(session.query(Item).filter_by(id = i).first())
    item_list = session.query(Item).all()
    item_size =  len(item_list)
    category_list = session.query(Category).all()
    for i in range(0,6):
        five_random_item.append(item_list[random.randint(0,item_size-1)])
    # Conditional for Login/Logout buttons
    if 'username' in login_session:
        log = True

    return render_template('landing_page.html', items = five_random_item, categorys = category_list, log = log)

@app.route('/category/<int:category_id>')
def render_category_page(category_id):
    log = ''
    # Conditional for Login/Logout buttons
    if 'username' in login_session:
        log = True

    category = session.query(Category).filter_by(id = category_id).first()
    items = session.query(Item).filter_by(category_id = category_id).all()
    first_items = items[0:5]
    return render_template('category_page.html', category = category, items = first_items, log = log)

@app.route('/category/<int:category_id>/item/<int:item_id>')
def render_item_page(category_id,item_id):
    log = ''
    # Conditional for Login/Logout buttons
    if 'username' in login_session:
        log = True

    category = session.query(Category).filter_by(id = category_id).first()
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('item_page.html', category = category, item= item, log = log)

@app.route('/category/<int:category_id>/item/new')
def render_add_new_item_page(category_id):
    log = ''
    # Conditional for Login/Logout buttons
    if 'username' not in login_session:
        flash("You're Not Logged in, please Log in!")
        return redirect(url_for('render_landing_page'), code=302)
    else: 
        log = True

    category = session.query(Category).filter_by(id = category_id).first()
    return render_template('add_new_item_page.html', category = category, log = log)

@app.route('/category/<int:category_id>/item/<int:item_id>/edit', methods=['GET','POST'])
def edit_item(item_id, category_id):
    item = session.query(Item).filter_by(id = item_id).one()
    item_user = item.user
    log = ''
    # Conditional for Login/Logout buttons
    if 'username' not in login_session:
        flash("You're Not Logged in, please Log in!")
        return redirect(url_for('render_landing_page'), code=302)
    # Conditional for Item Ownership
    elif login_session != item_user:
        flash('You cannot edit this item, because you are not owner!')
        log = False
        return redirect(url_for('render_landing_page'), code=302)
    # If User passes everything then Render Edit Template
    else:
        log = True
        return render_template('edit_item.html', item = item, log = log)

        

    

@app.route('/category/<int:category_id>/item/<int:item_id>/delete')
def delete_item(item_id, category_id):
    log = ''
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('delete_item.html', item = item, log=log)

@app.route('/logout', methods=['POST'])
def logout():
    login_session.pop('username', None)
    login_session.pop('image_url',None)
    login_session.pop('id_token', None)
    return redirect('/',code=302)    



if __name__ == '__main__':
    app.debug = True
    # app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
