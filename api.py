from flask import Flask,request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
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

class HelloWorld(Resource):
  def get(self):
    return {'msg':'Hello World!'}


class TodoSimple(Resource):
  def get(self,todo_id):
    return {todo_id:todos[todo_id]}

  def put(self,todo_id):
    todos[todo_id] = request.form['data']
    return {todo_id:todos[todo_id]}


class Todo(Resource):
  def get(self, todo_id):
    abort_if_not_found(todo_id)
    return TODOS[todo_id]

  def delete(self, todo_id):
    abort_if_not_found(todo_id)
    del TODOS[todo_id]
    return '', 204

  def put(self, todo_id):
    args = parser.parse_args()
    task = {'task': args['task']}
    TODOS[todo_id] = task
    return task, 201


class TodoList(Resource):
  def get(self):
    return TODOS

  def post(self):
    args = parser.parse_args()
    #print 'args', args
    #print TODOS.keys(),len(TODOS) 
    #todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
    todo_id = len(TODOS) + 1
    todo_id = 'todo%i' % todo_id
    TODOS[todo_id] = {'task': args['task']}
    return TODOS[todo_id], 201



api.add_resource(HelloWorld,'/')
#api.add_resource(TodoSimple,'/<string:todo_id>')
api.add_resource(TodoList,'/todos')
api.add_resource(Todo,'/todos/<todo_id>')


if __name__=='__main__':
  app.run(debug=True)
