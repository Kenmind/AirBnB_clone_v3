#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_get(self):
        """Test that get returns specific object, or none"""
        new_state = State(name="New York")
        new_state.save()
        new_user = User(email="bob@foobar.com", password="password")
        new_user.save()
        self.assertIs(new_state, models.storage.get("State", new_state.id))
        self.assertIs(None, models.storage.get("State", "blah"))
        self.assertIs(None, models.storage.get("blah", "blah"))
        self.assertIs(new_user, models.storage.get("User", new_user.id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_count(self):
        """test that new adds an object to the database"""
        initial_count = models.storage.count()
        self.assertEqual(models.storage.count("Blah"), 0)
        new_state = State(name="Florida")
        new_state.save()
        new_user = User(email="bob@foobar.com", password="password")
        new_user.save()
        self.assertEqual(models.storage.count("State"), initial_count + 1)
        self.assertEqual(models.storage.count(), initial_count + 2)


@unittest.skipIf(models.storage_t != 'db', "Testing file storage")
class TestFileStorage(unittest.TestCase):
    """Unittests for testing the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """FileStorage testing setup.
            Temporarily renames any existing file.json.
            Resets FileStorage objects dictionary.
            Creates instances of all class types for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base = BaseModel()
        key = "{}.{}".format(type(cls.base).__name__, cls.base.id)
        FileStorage._FileStorage__objects[key] = cls.base
        cls.user = User()
        key = "{}.{}".format(type(cls.user).__name__, cls.user.id)
        FileStorage._FileStorage__objects[key] = cls.user
        cls.state = State()
        key = "{}.{}".format(type(cls.state).__name__, cls.state.id)
        FileStorage._FileStorage__objects[key] = cls.state
        cls.place = Place()
        key = "{}.{}".format(type(cls.place).__name__, cls.place.id)
        FileStorage._FileStorage__objects[key] = cls.place
        cls.city = City()
        key = "{}.{}".format(type(cls.city).__name__, cls.city.id)
        FileStorage._FileStorage__objects[key] = cls.city
        cls.amenity = Amenity()
        key = "{}.{}".format(type(cls.amenity).__name__, cls.amenity.id)
        FileStorage._FileStorage__objects[key] = cls.amenity
        cls.review = Review()
        key = "{}.{}".format(type(cls.review).__name__, cls.review.id)
        FileStorage._FileStorage__objects[key] = cls.review

    @classmethod
    def tearDownClass(cls):
        """FileStorage testing teardown.
            Restore original file.json.
            Delete all test class instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.storage
        del cls.base
        del cls.user
        del cls.state
        del cls.place
        del cls.city
        del cls.amenity
        del cls.review

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        self.storage.save()
        with open("file.json", "r", encoding="utf-8") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + self.base.id, save_text)
            self.assertIn("User." + self.user.id, save_text)
            self.assertIn("State." + self.state.id, save_text)
            self.assertIn("Place." + self.place.id, save_text)
            self.assertIn("City." + self.city.id, save_text)
            self.assertIn("Amenity." + self.amenity.id, save_text)
            self.assertIn("Review." + self.review.id, save_text)


@unittest.skipIf(models.storage_t != 'db', 'skip if environ is not db')
class TestStorageGet(unittest.TestCase):
    """
    Testing `get()` method in DBStorage
    """

    def setUp(self):
        """
        setup method
        """
        self.state = State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """
        testing get() method
        :return: True if pass, else False
        """
        result = storage.get(cls="State", id=self.state.id)

        self.assertIsInstance(result, State)

    def test_get_method_return(self):
        """
        test get() method for matching id
        :return: True if pass, else False
        """
        result = storage.get(cls="State", id=str(self.state.id))

        self.assertEqual(self.state.id, result.id)

    def test_get_method_none(self):
        """
        testing get() method for None existing object
        :return: True if pass, else False
        """
        result = storage.get(cls="State", id="doesnotexist")

        self.assertIsNone(result)


@unittest.skipIf(models.storage_t != 'db', 'skip if environ is not db')
class TestStorageCount(unittest.TestCase):
    """
    tests count() method in DBStorage
    """

    def setup(self):
        """
        setup method
        """
        self.state1 = State(name="Zambia")
        self.state1.save()
        self.state2 = State(name="Nigeria")
        self.state2.save()
        self.state3 = State(name="Congo")
        self.state3.save()
        self.state4 = State(name="Kenya")
        self.state4.save()
        self.state5 = State(name="Rwanda")
        self.state5.save()
        self.state6 = State(name="Ghana")
        self.state6.save()
        self.state7 = State(name="Namibia")
        self.state7.save()

    def test_count_all(self):
        """
        test counting all objects in storage
        :return: True if pass, else False
        """
        result = storage.count()

        self.assertEqual(len(storage.all()), result)

    def test_count_state(self):
        """
        test counting all state instances
        :return: True if pass, else False
        """
        result = storage.count(cls="State")

        self.assertEqual(len(storage.all("State")), result)

    def test_count_city(self):
        """
        test counting non existent city
        :return: True if pass, else False
        """
        result = storage.count(cls="City")

        self.assertEqual(int(0 if len(storage.all("City")) is None else
                             len(storage.all("City"))), result)


if __name__ == "__main__":
    unittest.main
