#!/usr/bin/python3
"""
Create a new view for Place objects that handles
all default RESTFul API actions
"""
from flask import jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")
    user_id = data["user_id"]
    if not storage.get(User, user_id):
        abort(404)
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.get_json()
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Route to handle HTTP method for searching places based on criteria.
    """
    # Retrieve all places from storage
    all_places = storage.all('Place').values()

    # Parse request JSON
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')

    # Extract criteria from request JSON
    states = req_json.get('states', [])
    cities = req_json.get('cities', [])
    amenities = req_json.get('amenities', [])

    # Filter places based on states and cities
    filtered_places = []
    if states:
        state_cities = {city.id for state_id in states
                        for city in storage.get(State, state_id).cities}
        filtered_places.extend(place for place in
                               all_places if place.city_id in state_cities)
    if cities:
        city_set = {city_id for city_id in
                    cities if storage.get(City, city_id)}
        filtered_places.extend(place for place in
                               all_places if place.city_id in city_set)

    # Filter places based on amenities
    if amenities:
        amenity_ids = {amenity_id for amenity_id in amenities
                       if storage.get(Amenity, amenity_id)}
        filtered_places = [place for place in filtered_places
                           if all(amenity_id in
                                  {amenity.id for amenity in place.amenities}
                                  for amenity_id in amenity_ids)]

    # Convert filtered places to JSON and return response
    result = [place.to_json() for place in filtered_places]
    return jsonify(result)
