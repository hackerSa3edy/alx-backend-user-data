#!/usr/bin/env python3
""" Base module
This module defines a Base class that provides basic functionality for
creating, saving, loading, and managing objects with unique IDs and timestamps.
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base:
    """ Base class
    Provides methods for initializing, saving, loading, and managing objects.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Base instance
        Args:
            *args (list): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.
        """
        s_class = self.__class__.__name__
        if s_class not in DATA:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = self._parse_datetime(kwargs.get('created_at'))
        self.updated_at = self._parse_datetime(kwargs.get('updated_at'))

    def _parse_datetime(self, date_str: str) -> datetime:
        """ Parse a datetime string or return current UTC time if None
        Args:
            date_str (str): The datetime string to parse.
        Returns:
            datetime: The parsed datetime object or current UTC time.
        """
        if date_str:
            return datetime.strptime(date_str, TIMESTAMP_FORMAT)
        return datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Check equality with another Base instance
        Args:
            other (Base): The other instance to compare with.
        Returns:
            bool: True if both instances are equal, False otherwise.
        """
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert the object to a JSON dictionary
        Args:
            for_serialization (bool): Whether to include private attributes.
        Returns:
            dict: The JSON dictionary representation of the object.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            result[key] = (value.strftime(TIMESTAMP_FORMAT)
                           if isinstance(value, datetime)
                           else value)
        return result

    @classmethod
    def load_from_file(cls):
        """ Load all objects from file
        Loads all objects of the class from a JSON file and populates
        the DATA dictionary.
        """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """ Save all objects to file
        Saves all objects of the class to a JSON file from the DATA dictionary.
        """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {
            obj_id: obj.to_json(True)
            for obj_id, obj in
            DATA[s_class].items()
            }

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """ Save current object
        Updates the updated_at timestamp and saves the object to the DATA
        dictionary and file.
        """
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """ Remove object
        Removes the object from the DATA dictionary and updates the file.
        """
        s_class = self.__class__.__name__
        if self.id in DATA[s_class]:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ Count all objects
        Returns the number of objects of the class in the DATA dictionary.
        Returns:
            int: The count of objects.
        """
        return len(DATA[cls.__name__])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """ Return all objects
        Returns all objects of the class from the DATA dictionary.
        Returns:
            Iterable[Base]: An iterable of all objects.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """ Return one object by ID
        Args:
            id (str): The ID of the object to retrieve.
        Returns:
            Base: The object with the specified ID, or None if not found.
        """
        return DATA[cls.__name__].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """ Search all objects with matching attributes
        Args:
            attributes (dict): The attributes to match.
        Returns:
            List[Base]: A list of objects that match the given attributes.
        """
        def _search(obj):
            return all(getattr(obj, k) == v for k, v in attributes.items())

        return list(filter(_search, DATA[cls.__name__].values()))
