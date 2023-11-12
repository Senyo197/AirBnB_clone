#!/usr/bin/python
""" A File storage class"""

import json
from os.path import exists
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.review import Review


class FileStorage:
    """
    FileStorage class for serializing and deserializing objects to JSON

    Attributes:
        __file_path (str): The path to the JSON file
        __objects (dict): A dictionary to store serialized objects
        CLASSES (dict): A mapping of class names to their corresponding classes
    """
    __file_path = "file.json"
    __objects = {}

    CLASSES = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'Place': Place,
        'Amenity': Amenity,
        'City': City,
        'Review': Review,
    }

    def all(self):
        """ Retrieve and return all objects stored in __objects"""
        return self.__objects

    def new(self, obj):
        """Add a new object to __objects"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Save the serialized objects to the JSON file"""
        serialized_objs = {}
        for key, obj in self.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            json.dump(serialized_objs, file)

    def reload(self):
        """Reload objects from the JSON file into the __objects dictionary"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                deserialized_objs = json.load(file)
                for key, obj_data in deserialized_objs.items():
                    class_name, obj_id = key.split('.')
                    obj_instance = self.CLASSES[class_name](**obj_data)
                    self.__objects[key] = obj_instance
        except FileNotFoundError:
            pass
