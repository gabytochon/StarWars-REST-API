"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personaje, Planeta, Usuario
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
@app.route('/users', methods=['GET'])
def user_list():
    #obtener información de la base de datos
    get_usuario = Usuario.query.all()
    print(get_usuario)
    #convertir la data
    lista_usuario = list(map(lambda usuario: usuario.serialize_two(), get_usuario))
    print(lista_usuario)
    #enviar data
    return jsonify(lista_usuario), 200
@app.route('/users/<int:usuario_id>', methods=['GET'])
def users_favorites_list(usuario_id=None):
    if usuario_id is not None:
        get_usuario_favorito = Usuario.query.get(usuario_id)
        if get_usuario_favorito is not None:
            return jsonify(get_usuario_favorito.serialize())
        return jsonify("Not found"), 404
    else:
        return jsonify("Not found"), 404
@app.route('/people', methods=['GET'])
def people_list():
    #obtener información de la base de datos
    get_personaje = Personaje.query.all()
    print(get_personaje)
    #convertir la data
    lista_personajes = list(map(lambda personaje: personaje.serialize(), get_personaje))
    print(lista_personajes)
    #enviar data
    return jsonify(lista_personajes), 200
@app.route('/people/<int:people_id>', methods=['GET'])
def one_people(people_id=None):
    if people_id is not None:
        get_persona = Personaje.query.get(people_id)
        if get_persona is not None:
            return jsonify(get_persona.serialize())
        return jsonify("Not found"), 404
    else:
        return jsonify("Not found"), 404
@app.route('/planets', methods=['GET'])
def planets_list():
    #obtener información de la base de datos
    get_planeta = Planeta.query.all()
    print(get_planeta)
    #convertir la data
    lista_planeta = list(map(lambda planeta: planeta.serialize(), get_planeta))
    print(lista_planeta)
    #enviar data
    return jsonify(lista_planeta), 200
@app.route('/planets/<int:planet_id>', methods=['GET'])
def one_planet(planet_id=None):
    if planet_id is not None:
        get_planet = Planeta.query.get(planet_id)
        if get_planet is not None:
            return jsonify(get_planet.serialize())
        return jsonify("Not found"), 404
    else:
        return jsonify("Not found"), 404
@app.route('/people', methods=['POST'])
def post_people():
    body = request.json
    nuevo_personaje = Personaje.create_people(body)
    if not isinstance(nuevo_personaje, Personaje):
        print(type(nuevo_personaje), isinstance(nuevo_personaje, Personaje))
        return jsonify({
            "message": nuevo_personaje["message"]
        }), nuevo_personaje["status"]
    print(nuevo_personaje)
    return jsonify({
        "message": "Nuevo personaje agregado"
    }), 200
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)