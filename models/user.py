#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password_hash(self):
        """
        getter for password
        :return: hashed password
        """
        return self.__dict__.get("password")

    @password_hash.setter
    def password_hash(self, password):
        from hashlib import md5
        """
            pssword setter, with md5 hashing
            :param password: password
            :return: nothing
        """
        self.__dict__["password"] = md5(password.encode('utf-8')).hexdigest()
