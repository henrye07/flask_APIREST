from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
# ESQUEMA PARA INTERACTUAR
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# --------------------------------- SQLALCHEMY-----------------------
        # ------------DIRECCION DE LA BBDD
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_db' 
                                    # mysql+otro modulo que vamos a usar://usuario:contraseña@direccion/nombre_de_la_BBDD
        # ------------CONFIGURACION POR DEFECTO EN CASOS DE ERROR 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
                            
# ------------PARA INSTANCIAR Y ME DEVUELVA UNA BBDD
db = SQLAlchemy(app)
ma = Marshmallow(app)

# MODELO PARA CREAR UNA TABLA
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(70),unique=True)
    description=db.Column(db.String(100))

    def __init__(self,title,description):
        self.title=title
        self.description=description
    
db.create_all()

class taskSchema(ma.Schema):
    class Meta:
        fields= ('id','title','description')

task_schema=taskSchema()
tasks_schema=taskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():

    title=request.json['title']
    description=request.json['description']

    new_task=Task(title,description)
    db.session.add(new_task)
    db.session.commit()

    # print(request.json)
    # return 'Received'

    return task_schema.jsonify(new_task)
    
        

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks=Task.query.all()
    result = tasks_schema.dump(all_tasks)

    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task_get=Task.query.get(id)

    return task_schema.jsonify(task_get)   

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task=Task.query.get(id)
    title=request.json['title']
    description=request.json['description']

    task.title=title
    task.description=description
    db.session.commit()
    return task_schema.jsonify(task) 

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task=Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task) 

if __name__=='__main__':
    app.run(debug=True)