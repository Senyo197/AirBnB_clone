#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(User, type(User()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(User(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(User().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def testEmailIsPublicStr(self):
        self.assertEqual(str, type(User.email))

    def testPasswordIsPublicStr(self):
        self.assertEqual(str, type(User.password))

    def testFirstNameIsPublicStr(self):
        self.assertEqual(str, type(User.first_name))

    def testLastNameIsPublicStr(self):
        self.assertEqual(str, type(User.last_name))

    def testTwoUsersUniqueIds(self):
        us1 = User()
        us2 = User()
        self.assertNotEqual(us1.id, us2.id)

    def testTwoUsersDifferentCreatedAt(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def testTwoUsersDifferentUpdatedAt(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def testStrRepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        us_str = us.__str__()
        self.assertIn("[User] (123456)", us_str)
        self.assertIn("'id': '123456'", us_str)
        self.assertIn("'created_at': " + dt_repr, us_str)
        self.assertIn("'updated_at': " + dt_repr, us_str)

    def testArgsUnused(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def testInstantiationWithKwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        us = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Unittests for testing save method of the User class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testOneSave(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def testTwoSaves(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def testSaveWithArg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def testSaveUpdatesFile(self):
        us = User()
        us.save()
        us_id = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(us_id, f.read())


class TestUserToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def testToDictType(self):
        self.assertTrue(dict, type(User().to_dict()))

    def testToDictContainsCorrectKeys(self):
        us = User()
        self.assertIn("id", us.to_dict())
        self.assertIn("created_at", us.to_dict())
        self.assertIn("updated_at", us.to_dict())
        self.assertIn("__class__", us.to_dict())

    def testToDictContainsAddedAttributes(self):
        us = User()
        us.middle_name = "Holberton"
        us.my_number = 98
        self.assertEqual("Holberton", us.middle_name)
        self.assertIn("my_number", us.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        us = User()
        us_dict = us.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    def testToDictOutput(self):
        dt = datetime.today()
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), t_dict)

    def testContrastToDictDunderDict(self):
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def testToDictWithArg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()

