#!/usr/bin/python
import json
from models.base_model import BaseModel


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        serialized_objs = {}
        for key, obj in self.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objs, file)

    def reload(self):
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
            for key, value in data.items():
                class_name, obj_id = key.split('.')
                obj = base.from_dict(value)
                self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def __init__(self):
        self.reload()
