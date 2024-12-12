"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['GET'])
def handle_login():
    usuarios = User.query.all()
    if usuarios == []:
        return jsonify({"msg":"No existen usuarios"}), 404
    response_body = [item.serialize() for item in usuarios]
    return jsonify(response_body), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"msg":"No existe el usuario"}), 404
    return jsonify(user.serialize()), 200


@app.route('/people', methods=['GET'])
def get_people():
    personajes = People.query.all()
    if personajes == []:
        return jsonify({"msg":"No existen personajes"}), 404
    response_body = [item.serialize() for item in personajes]
    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    personaje = People.query.filter_by(id=people_id).first()
    if personaje is None:
        return jsonify({"msg":"No existe el personaje"}), 404
    return jsonify(personaje.serialize()), 200


@app.route('/planet', methods=['GET'])
def get_planets():
    planetas = Planet.query.all()
    if planetas == []:
        return jsonify({"msg":"No existen planetas"}), 404
    response_body = [item.serialize() for item in planetas]
    return jsonify(response_body), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planeta = Planet.query.filter_by(id=planet_id).first()
    if planeta is None:
        return jsonify({"msg":"No existe el planeta"}), 404
    return jsonify(planeta.serialize()), 200


@app.route('/favorites', methods=['GET'])
def get_favorite():
    favoritos = Favorite.query.all()
    if favoritos == []:
        return jsonify({"msg":"No existen favoritos"}), 404
    response_body = [item.serialize() for item in favoritos]
    return jsonify(response_body), 200


@app.route('/favorites/<int:favorite_id>', methods=['GET'])
def get_favorite_id(favorite_id):
    favorito = Favorite.query.filter_by(id=favorite_id).first()
    if favorito is None:
        return jsonify({"msg":"No existe el favorito"}), 404
    return jsonify(favorito.serialize()), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    body = request.json
    email = body.get("email")
    user = User.query.filter_by(email=email).one_or_none()
    if user == None:
        return jsonify({"msg":"No existe el usuario"}), 404
    
    planeta = Planet.query.get(planet_id)
    if planeta == None:
        return jsonify({"msg":"No existe el planeta"}), 404

    new_favorite = Favorite()
    new_favorite.user = user
    new_favorite.planet = planeta
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_favorite_people(people_id):
    body = request.json
    email = body.get("email")
    user = User.query.filter_by(email=email).one_or_none()
    if user == None:
        return jsonify({"msg":"No existe el usuario"}), 404
    
    personaje = People.query.get(people_id)
    if personaje == None:
        return jsonify({"msg":"No existe el personaje"}), 404

    new_favorite = Favorite()
    new_favorite.user = user
    new_favorite.people = personaje
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    body = request.json
    email = body.get("email")
    user = User.query.filter_by(email=email).one_or_none()
    if user == None:
        return jsonify({"msg":"No existe el usuario"}), 404
    
    planeta = Planet.query.get(planet_id)
    if planeta == None:
        return jsonify({"msg":"No existe el planeta"}), 404

    favorite_to_delete = Favorite.query.filter_by(user_id=user.id, planet_id=planeta.id).first()
    if favorite_to_delete == None:
        return jsonify({"msg":"No existe el planeta favorito"}), 404

    db.session.delete(favorite_to_delete)
    db.session.commit()

    return jsonify({"msg":"Eliminado con éxito"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    body = request.json
    email = body.get("email")
    user = User.query.filter_by(email=email).one_or_none()
    if user == None:
        return jsonify({"msg":"No existe el usuario"}), 404
    
    personaje = People.query.get(people_id)
    if personaje == None:
        return jsonify({"msg":"No existe el personaje"}), 404

    favorite_to_delete = Favorite.query.filter_by(user_id=user.id, people_id=personaje.id).first()
    if favorite_to_delete == None:
        return jsonify({"msg":"No existe el personaje favorito"}), 404

    db.session.delete(favorite_to_delete)
    db.session.commit()

    return jsonify({"msg":"Eliminado con éxito"}), 200

