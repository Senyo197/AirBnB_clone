#!/usr/bin/python
import json
from os.path import exists
from models.base_model import BaseModel

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__,obj.id)
        self.__objects[key] = obj

    def save(self):
        serialized_objs = {}
        for key, obj in self.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objs, file)

    def reload(self):
        if exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                deserialized_objs = json.load(file)
                for key, obj_data in deserialized_objs.items():
                    class_name, obj_id = key.split('.')
                    class_instance = globals()[class_name]
                    obj_instance = class_instance(**obj_data)
                    self.__objects[key] = obj_instance
