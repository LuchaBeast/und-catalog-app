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
