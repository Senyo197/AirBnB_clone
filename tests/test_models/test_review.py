#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReviewInstantiation
    TestReviewSave
    TestReviewToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReviewInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(Review, type(Review()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(Review(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(Review().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def testPlaceIdIsPublicClassAttribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rv))
        self.assertNotIn("place_id", rv.__dict__)

    def testUserIdIsPublicClassAttribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rv))
        self.assertNotIn("user_id", rv.__dict__)

    def testTextIsPublicClassAttribute(self):
        rv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rv))
        self.assertNotIn("text", rv.__dict__)

    def testTwoReviewsUniqueIds(self):
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def testTwoReviewsDifferentCreatedAt(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def testTwoReviewsDifferentUpdatedAt(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def testStrRepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        rv_str = rv.__str__()
        self.assertIn("[Review] (123456)", rv_str)
        self.assertIn("'id': '123456'", rv_str)
        self.assertIn("'created_at': " + dt_repr, rv_str)
        self.assertIn("'updated_at': " + dt_repr, rv_str)

    def testArgsUnused(self):
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def testInstantiationWithKwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(rv.id, "345")
        self.assertEqual(rv.created_at, dt)
        self.assertEqual(rv.updated_at, dt)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSave(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)

    def testTwoSaves(self):
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        second_updated_at = rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rv.save()
        self.assertLess(second_updated_at, rv.updated_at)

    def testSaveWithArg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)

    def testSaveUpdatesFile(self):
        rv = Review()
        rv.save()
        rv_id = "Review." + rv.id
        with open("file.json", "r") as f:
            self.assertIn(rv_id, f.read())


class TestReviewToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def testToDictType(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def testToDictContainsCorrectKeys(self):
        rv = Review()
        self.assertIn("id", rv.to_dict())
        self.assertIn("created_at", rv.to_dict())
        self.assertIn("updated_at", rv.to_dict())
        self.assertIn("__class__", rv.to_dict())

    def testToDictContainsAddedAttributes(self):
        rv = Review()
        rv.middle_name = "Holberton"
        rv.my_number = 98
        self.assertEqual("Holberton", rv.middle_name)
        self.assertIn("my_number", rv.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        rv = Review()
        rv_dict = rv.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def testToDictOutput(self):
        dt = datetime.today()
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(rv.to_dict(), t_dict)

    def testContrastToDictDunderDict(self):
        rv = Review()
        self.assertNotEqual(rv.to_dict(), rv.__dict__)

    def testToDictWithArg(self):
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()

