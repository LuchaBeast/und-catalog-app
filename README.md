# Catalog app for Udacity Nanodegree project

README needs to be fleshed out...

## To get started
* Run database_setup.py to create the sqlite database
* Run add_catalog_content.py to insert dummy catalog data into the database
* Run catalog.py start the catalog app and access it via localhost

## Functionality
* To add a new item to the catalog, visit the following url path - /cat/<int:category_id>/new-item/
** Example: localhost:5000/cat/1/new-item/
* To edit an existing item in the catalog, visit the following url path - /cat/<int:category_id>/i/<int:id>/edit-item/
** Example: localhost:5000/cat/1/i/1/edit-item/
** You can edit just the title, the description or both
* To delete an item from the catalog, visit the following url path - /cat/<int:category_id>/i/<int:id>/delete-item/
** Example: localhost:5000/cat/1/i/1/delete-item/
* To view category and product info in JSON format
** /cat/<int:category_id>/json/
** /cat/<int:category_id>/i/<int:id>/json/

## Things to be added
* Working Google sign in functionality
* When Google sign in functionality is fixed, place adding, editing and deleting items behind authentication, so only authorized users can modify products and categories.
