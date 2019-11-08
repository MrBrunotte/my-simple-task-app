import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'task_manager'
app.config['MONGO_URI'] = 'mongodb+srv://mrbrunotte:mrUSERbrunotte@foodictionary-gckbp.mongodb.net/task_manager?retryWrites=true&w=majority'
# Insert password and change test to db name (task_manager) change this to environment variables!!

# add instance of pymongo
mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())
    # returns everything from tasks in task_manager DB


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)
