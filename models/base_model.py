#!/usr/bin/python3
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
    tform = "%Y-%m-%dT%H:%M:%S.%f"
    self.id = str(uuid4())
    self.created_at = datetime.today()
    self.updated_at = datetime.today()
    if len(kwargs) != 0:
        for k, v in kwargs.items():
            if k != "__class__":
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, tform)
                else:
                    self.__dict__[k] = v
    else:
        models.storage.new(self)
 

    def __str__(self):
        return f"[self.__class__.__name__] ({self.id}) {self.__dict__}"

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
