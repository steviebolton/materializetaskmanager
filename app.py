import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "task_manager" 
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route("/")
@app.route("/get_tasks")
@app.route("/get_tasks_by_category/<category_name>")
def get_tasks(category_name=None):
    if category_name:
        tasks=mongo.db.tasks.find({"category_name": category_name})
    else:
        tasks=mongo.db.tasks.find()
        
    return render_template("tasks.html", tasks=tasks)


@app.route("/add_task")
def add_task():
    categories = mongo.db.categories.find()
    return render_template("addtask.html", categories=categories)


@app.route("/insert_task", methods=['POST'])
def insert_task():
    mongo.db.tasks.insert_one(request.form.to_dict())
    return redirect(url_for("get_tasks"))

    
@app.route("/edit_task/<task_id>")
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    categories = mongo.db.categories.find()
    return render_template("edittask.html", task=the_task, categories=categories)


@app.route("/update_task/<task_id>", methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({"_id": ObjectId(task_id)}, request.form.to_dict())
    return redirect(url_for("get_tasks"))
    

@app.route("/delete_task", methods=["POST"])
def delete_task():
    task_id = request.form['task_id']
    mongo.db.tasks.remove({"_id":ObjectId(task_id)})
    return redirect(url_for("get_tasks"))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())
    

@app.route('/new_category')
def new_category():
    return render_template('addcategory.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    categories.insert_one(request.form.to_dict())
    return redirect(url_for('get_categories'))
    

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))

  
@app.route('/delete_category/<category_id>')  
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))
    




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

