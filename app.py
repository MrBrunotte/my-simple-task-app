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
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)}) # we look for one task and we search by "id" in the "ObjectId" (red) in the DB
    all_categories = mongo.db.categories.find() 
    # create a list of the collections so that we can find the task that we want to edit with all its categories
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
