#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCityInstantiation
    TestCitySave
    TestCityToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(City, type(City()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(City(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(City().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def testStateIdIsPublicClassAttribute(self):
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def testNameIsPublicClassAttribute(self):
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def testTwoCitiesUniqueIds(self):
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def testTwoCitiesDifferentCreatedAt(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def testTwoCitiesDifferentUpdatedAt(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def testStrRepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cy_str = cy.__str__()
        self.assertIn("[City] (123456)", cy_str)
        self.assertIn("'id': '123456'", cy_str)
        self.assertIn("'created_at': " + dt_repr, cy_str)
        self.assertIn("'updated_at': " + dt_repr, cy_str)

    def testArgsUnused(self):
        cy = City(None)
        self.assertNotIn(None, cy.__dict__.values())

    def testInstantiationWithKwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "345")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def testTwoSaves(self):
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def testSaveWithArg(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def testSaveUpdatesFile(self):
        cy = City()
        cy.save()
        cy_id = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cy_id, f.read())


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def testToDictType(self):
        self.assertTrue(dict, type(City().to_dict()))

    def testToDictContainsCorrectKeys(self):
        cy = City()
        self.assertIn("id", cy.to_dict())
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())

    def testToDictContainsAddedAttributes(self):
        cy = City()
        cy.middle_name = "Holberton"
        cy.my_number = 98
        self.assertEqual("Holberton", cy.middle_name)
        self.assertIn("my_number", cy.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def testToDictOutput(self):
        dt = datetime.today()
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), t_dict)

    def testContrastToDictDunderDict(self):
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def testToDictWithArg(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()

