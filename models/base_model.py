#!/usr/bin/python3
import models
from datetime import datetime
import uuid


class BaseModel:
    """Represents the BaseModel for AirBnB clone the console project."""

    def __init__(self, *args, **kwargs):
        """Initializing a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        setattr(self, key,
                                datetime.strptime(value, time_format))
                    else:
                        setattr(self, key, value)
                else:
                    models.storage.new(self)

    def __str__(self):
        return f"[self.__class__.__name__] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
