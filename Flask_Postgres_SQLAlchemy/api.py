from flask import Flask,request
from flask_restful import Resource, Api, reqparse, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aronepremkumar@localhost/postgres'
db = SQLAlchemy(app)
api = Api(app)

todos = {}

TODOS = {
  'todos1':{'task':'Flask restful API'},
  'todos2':{'task':'Database should be Postgresql'},
  'todos3':{'task':'Hope this shines well!'}
}

def abort_if_not_found(todo_id):
  if todo_id not in TODOS:
    abort(404,message="Sorry todo {} doesn't exist.".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('id')

class HelloWorld(Resource):
  def get(self):
    return {'msg':'Hello World!'}


class Task(db.Model):
  __tablename__ = 'Task'
  todo_id = db.Column(db.String(20),primary_key=True)
  task = db.Column(db.String(80))
 
  
  def __init__(self,todo_id,task):
    self.task = task
    self.todo_id = todo_id
  
  #todo_id = db.Column(db.String(20),primary_key=True)
  #task = db.Column(db.String(80))

  def __repr__(self):
    return '<Task %r>' % self.todo_id

class TodoSimple(Resource):
  def get(self,todo_id):
    return {todo_id:todos[todo_id]}
    #print 'Here in todo simple'
    #print 'Todo id', todo_id
    #task = Task.query.filter_by(todo_id=todo_id).first_or_404()
    #print task
    #return{todo_id:'Here in todo simple'}
    #return {todo_id:todos[todo_id]}

  def put(self,todo_id):
    todos[todo_id] = request.form['data']
    return {todo_id:todos[todo_id]}


class Todo(Resource):
  def get(self, todo_id):
    #abort_if_not_found(todo_id)
    task = Task.query.filter_by(todo_id=todo_id).first_or_404()
    return {todo_id:task.task}

  def delete(self, todo_id):
    #abort_if_not_found(todo_id)
    task = Task.query.filter_by(todo_id=todo_id).first_or_404()
    delete_task = Task(todo_id,task.task)
    db.session.delete(delete_task)
    db.session.commit()
    return '', 204

  def put(self, todo_id):
    args = parser.parse_args()
    update_task = Task(todo_id,args['task'])
    db.session.query.filter_by(todo_id=todo_id).update(update_task)
    return task, 201


class TodoList(Resource):
  def get(self):
    tasks = Task.query.all()
    task_dict = {}
    for task in tasks:
      task_dict[task.todo_id] = task.task
    return task_dict

  def post(self):
    args = parser.parse_args()
    id = int(args['id'])
    #tasks = Task.query.all()
    #todo_id = len(tasks) + 1
    todo_id = id
    todo_id = 'todo%i' % todo_id
    new_task = Task(todo_id,args['task'])
    db.session.add(new_task)
    db.session.commit()
    return_dict = {}
    return_dict[todo_id] = args['task']
    return return_dict
   



api.add_resource(HelloWorld,'/')
#api.add_resource(TodoSimple,'/<string:todo_id>')
api.add_resource(TodoList,'/todos')
api.add_resource(Todo,'/todos/<todo_id>')


if __name__=='__main__':
  app.run(debug=True)
