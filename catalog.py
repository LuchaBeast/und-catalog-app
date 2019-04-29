from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

app = Flask(__name__)

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
        return redirect(url_for('category', category_id=category_id))
    else:
        return render_template('new-item.html',
                               all_categories=all_categories,
                               category=category)

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
@app.route('/cat/<int:category_id>/i/<int:id>/edit-item/', methods=['GET', 'POST'])
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
        item_name=request.form['item_name']
        item_description=request.form['item_description']
        if item_name != '' and item_description != '':
            itemToEdit.item_name = item_name
            itemToEdit.item_description = item_description
        elif item_name != '' and item_description == '':
            itemToEdit.item_name = item_name
        elif item_name == '' and item_description != '':
            itemToEdit.item_description = item_description
        session.add(itemToEdit)
        session.commit()
        return redirect(url_for('item', category_id=category_id, id=id))
    else:
        return render_template('edit-item.html',
                               all_categories=all_categories,
                               category=category,
                               item=item)

# Create route for deleting item
@app.route('/cat/<int:category_id>/i/<int:id>/delete-item/', methods=['GET', 'POST'])
def deleteItem(category_id, id):
    all_categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    item = (session.query(Item)
            .filter_by(category_id=category_id)
            .filter_by(id=id)
            .one())
    return render_template('delete-item.html',
                           all_categories=all_categories,
                           category=category,
                           item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
