from flask import Flask, redirect, render_template, request, url_for, flash, \
    jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, httplib2, json, requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create homepage route
# Define variables necessary for populating the homepage
@app.route('/')
def homepage():
    all_categories = session.query(Category).all()
    all_items = session.query(Item).all()
    return render_template('index.html',
                           all_categories=all_categories,
                           all_items=all_items)

@app.route('/login/')
def showLogin():
    route = 'login'
    all_categories = session.query(Category).all()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html',
                           route=route,
                           all_categories=all_categories,
                           STATE=state)

@app.route('/googleconnect', methods=['POST'])
def googleconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user id doesn't match given user id."), 401)
        response.headers['Content-Type'] = 'applicaton/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client id does not match"), 401)
        print("Token's client id does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already logged in'), 200)
        response.headers['Content-Type'] = 'application/json'

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

@app.route('/googledisconnect')
def googledisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
    return response

# Create json route for categories
@app.route('/cat/<int:category_id>/json/')
def categoryJSON(category_id):
    items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(CategoryItems=[i.serialize for i in items])

# Create category route
# Define variables necessary for populating category page
@app.route('/cat/<int:category_id>/')
def category(category_id):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    return render_template('category.html',
                           all_categories=all_categories,
                           category=category,
                           items=items)

# Create new item route
@app.route('/cat/<int:category_id>/new-item/', methods=['GET', 'POST'])
def newItem(category_id):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = Item(item_name=request.form['item_name'],
                       item_description=request.form['item_description'],
                       category_id=category_id)
        session.add(newItem)
        session.commit()
        flash("Your new toy has been added to the catalog.")
        return redirect(url_for('category', category_id=category_id))
    else:
        return render_template('new-item.html',
                               all_categories=all_categories,
                               category=category)

# Create json route for individual items
@app.route('/cat/<int:category_id>/i/<int:id>/json/')
def itemJSON(category_id, id):
    item = (session.query(Item)
            .filter_by(category_id=category_id)
            .filter_by(id=id)
            .one())
    return jsonify(Item=item.serialize)

# Create item route
# Define variables necessary to populate item page
@app.route('/cat/<int:category_id>/i/<int:id>/')
def item(category_id, id):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = (session.query(Item)
            .filter_by(category_id=category_id)
            .filter_by(id=id)
            .one())
    return render_template('item.html',
                           all_categories=all_categories,
                           category=category,
                           item=item)


# Create edit item route
@app.route('/cat/<int:category_id>/i/<int:id>/edit-item/',
           methods=['GET', 'POST'])
def editItem(category_id, id):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = (session.query(Item)
            .filter_by(category_id=category_id)
            .filter_by(id=id)
            .one())
    itemToEdit = (session.query(Item)
                  .filter_by(id=id)
                  .one())
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        if item_name != '' and item_description != '':
            itemToEdit.item_name = item_name
            itemToEdit.item_description = item_description
            flash("Item name and description have been \
                   updated to reflect your changes.")
        elif item_name != '' and item_description == '':
            itemToEdit.item_name = item_name
            flash("Item name has been updated to reflect your changes.")
        elif item_name == '' and item_description != '':
            itemToEdit.item_description = item_description
            flash("Item description has been updated to reflect your changes.")
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('item', category_id=category_id, id=id))
    else:
        return render_template('edit-item.html',
                               all_categories=all_categories,
                               category=category,
                               item=item)

# Create route for deleting item
@app.route('/cat/<int:category_id>/i/<int:id>/delete-item/',
           methods=['GET', 'POST'])
def deleteItem(category_id, id):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = (session.query(Item)
            .filter_by(category_id=category_id)
            .filter_by(id=id)
            .one())
    itemToDelete = (session.query(Item)
                    .filter_by(id=id)
                    .one())
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Toy has been deleted from the catalog")
        return redirect(url_for('category', category_id=category_id))
    else:
        return render_template('delete-item.html',
                               all_categories=all_categories,
                               category=category,
                               item=item)


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
