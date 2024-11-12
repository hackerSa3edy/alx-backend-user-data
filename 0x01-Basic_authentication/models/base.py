#!/usr/bin/env python3
"""Base Module for Data Storage and Management."""

from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base:
    """Base class for data storage and persistence."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a new Base instance."""
        s_class = self.__class__.__name__
        DATA.setdefault(s_class, {})

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = (
            datetime.strptime(kwargs['created_at'], TIMESTAMP_FORMAT)
            if 'created_at' in kwargs
            else datetime.utcnow()
        )
        self.updated_at = (
            datetime.strptime(kwargs['updated_at'], TIMESTAMP_FORMAT)
            if 'updated_at' in kwargs
            else datetime.utcnow()
        )

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Compare two Base instances for equality."""
        return isinstance(other, Base) and self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """Convert the instance to a JSON-compatible dictionary."""
        return {
            key: value.strftime(TIMESTAMP_FORMAT)
            if isinstance(value, datetime) else value
            for key, value in self.__dict__.items()
            if for_serialization or not key.startswith('_')
        }

    @classmethod
    def load_from_file(cls):
        """Load all instances from the corresponding JSON file."""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}

        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            DATA[s_class] = {
                obj_id: cls(**obj_json)
                for obj_id, obj_json in json.load(f).items()
            }

    @classmethod
    def save_to_file(cls):
        """Save all instances to a JSON file."""
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"

        with open(file_path, 'w') as f:
            json.dump(
                {obj_id: obj.to_json(True)
                 for obj_id, obj in DATA[s_class].items()},
                f
            )

    def save(self):
        """Save the current instance."""
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """Remove the current instance from storage."""
        s_class = self.__class__.__name__
        if self.id in DATA[s_class]:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """Count the number of instances of this class."""
        return len(DATA.get(cls.__name__, {}))

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Retrieve all instances of this class."""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Retrieve an instance by its ID."""
        return DATA.get(cls.__name__, {}).get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search for instances matching given attributes."""
        if not attributes:
            return list(DATA.get(cls.__name__, {}).values())

        return [
            obj for obj in DATA.get(cls.__name__, {}).values()
            if all(getattr(obj, k) == v for k, v in attributes.items())
        ]
