#!/usr/bin/python3
"""Defining a new class called city."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represent the class city.

    Attributes:
        state_id (str): The state id.
        name (str): The name of the city.
    """

    state_id = ""
    name = ""
