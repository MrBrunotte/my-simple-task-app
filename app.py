import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'task_manager'
#app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost')
app.config['MONGO_URI'] = 'mongodb+srv://mrbrunotte:mrUSERbrunotte@foodictionary-gckbp.mongodb.net/task_manager?retryWrites=true&w=majority'
# Insert password and change test to db name (task_manager) change this to environment variables!!

# add instance of pymongo
mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())
    # returns everything from tasks in task_manager DB


@app.route('/add_task')
def add_task():
    return render_template('addtask.html', categories=mongo.db.categories.find())
    # we need to return the categories (categories is the collection name) from the db to the addtask.html

# since we are submitting a post we need the HTTP method POST!
@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    # We insert the user input into the form
    # Any of the form fields that have data inside them (or are active), will be submitted as part of the submission,
    # will go on to create a new document in the tasks collection in the task_manager DB
    # VIKTIGT: We need some validation fields here and in the HTML file for required fields
    return redirect(url_for('get_tasks'))


# wire up the edit button, we use the ObjectId from the bson.objectid library
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    # we look for one task and we search by "id" in the "ObjectId" (red) in the DB
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    # create a list of the collections so that we can find the task that we want to edit with all its categories
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)

# Update Task In The Database
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):   # we pass in the task ID because thats our hook into the primary key
    tasks = mongo.db.tasks  # we access the tasks collection
    tasks.update({'_id': ObjectId(task_id)},   # we call the update function, we specify the id as our key
                 {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))

# Delete Task
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)}
                          )  # use the remove function
    # redirect to get_tasks to see that it is removed!
    return redirect(url_for('get_tasks'))

# Display Categories
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html', categories=mongo.db.categories.find())


# we pass in the category ID into the function "edit_category()"
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

# Update Category In The Database
# <category_id> targets the correct document in the DB
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        # identify the ID and the field (category_name) that we want to update
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    # return to the categories with the get_categories function
    return redirect(url_for('get_categories'))


# Add Category pt2. This function inserts the category the function below that lets us add a new category
# no ID since it doesnt exist yet!!
@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    # add the category_doc into our colleciton (categories table)
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))

# Add Category pt1 this lets us add a new category
@app.route('/add_category')     
def add_category():
    return render_template('addcategory.html') # directs us to the addcategory page with the add_category function


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
