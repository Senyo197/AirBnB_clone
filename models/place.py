#!/usr/bin/python3
"""Defining a new class called place."""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represent a place.

    Attributes:
        city_id (str): The id of the city.
        user_id (str): The id of the user.
        name (str): The place name.
        description (str): The place description  place.
        number_rooms (int): The place number of rooms.
        number_bathrooms (int): The place number of bathrooms.
        max_guest (int): The place maximum number of guests.
        price_by_night (int): The place price by night.
        latitude (float): The place latitude.
        longitude (float): The place longitude.
        amenity_ids (list): A list of Amenity ids.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
