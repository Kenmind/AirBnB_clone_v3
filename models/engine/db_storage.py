#!/usr/bin/python3
"""
Contains the class DBStorage
"""

<<<<<<< HEAD
import models
import json
=======

>>>>>>> 393c1feee075498392811f7b90a27c4f82cef5fa
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user,passwd, host, database))
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        objects = {}
        if not self.__session:
            self.reload()
        if type(cls) == str:
            cls = classes.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + "." + obj.id] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + "." + obj.id] = obj
        return (objects)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def get(self, cls, id):
        """ retrives one object
            :param cls: class of object as string
            :param id: id of object as string
            :return: found object or None
        """
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in name2class:
            cls = name2class[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
<<<<<<< HEAD
        """Count number of objects in storage"""
        '''total = 0
=======
        """
            count the number of objects in storage:
            :param cls: class name
            :return: count of instances of a class
        """
        total = 0
>>>>>>> 393c1feee075498392811f7b90a27c4f82cef5fa
        if type(cls) == str and cls in name2class:
            cls = name2class[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in name2class.values():
                total += self.__session.query(cls).count()'''
        return len(self.all(cls))
