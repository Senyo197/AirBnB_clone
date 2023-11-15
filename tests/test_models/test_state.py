#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestStateInstantiation
    TestStateSave
    TestStateToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(State, type(State()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(State(), models.storage.all().values())

    def testIdIsPublicStr(self):
        self.assertEqual(str, type(State().id))

    def testCreatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def testUpdatedAtIsPublicDatetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def testNameIsPublicClassAttribute(self):
        st = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(st))
        self.assertNotIn("name", st.__dict__)

    def testTwoStatesUniqueIds(self):
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def testTwoStatesDifferentCreatedAt(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def testTwoStatesDifferentUpdatedAt(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def testStrRepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        st_str = st.__str__()
        self.assertIn("[State] (123456)", st_str)
        self.assertIn("'id': '123456'", st_str)
        self.assertIn("'created_at': " + dt_repr, st_str)
        self.assertIn("'updated_at': " + dt_repr, st_str)

    def testArgsUnused(self):
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def testInstantiationWithKwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        st = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(st.id, "345")
        self.assertEqual(st.created_at, dt)
        self.assertEqual(st.updated_at, dt)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        self.assertLess(first_updated_at, st.updated_at)

    def testTwoSaves(self):
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        st.save()
        self.assertLess(second_updated_at, st.updated_at)

    def testSaveWithArg(self):
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def testSaveUpdatesFile(self):
        st = State()
        st.save()
        st_id = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(st_id, f.read())


class TestStateToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def testToDictType(self):
        self.assertTrue(dict, type(State().to_dict()))

    def testToDictContainsCorrectKeys(self):
        st = State()
        self.assertIn("id", st.to_dict())
        self.assertIn("created_at", st.to_dict())
        self.assertIn("updated_at", st.to_dict())
        self.assertIn("__class__", st.to_dict())

    def testToDictContainsAddedAttributes(self):
        st = State()
        st.middle_name = "Holberton"
        st.my_number = 98
        self.assertEqual("Holberton", st.middle_name)
        self.assertIn("my_number", st.to_dict())

    def testToDictDatetimeAttributesAreStrs(self):
        st = State()
        st_dict = st.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def testToDictOutput(self):
        dt = datetime.today()
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        t_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(st.to_dict(), t_dict)

    def testContrastToDictDunderDict(self):
        st = State()
        self.assertNotEqual(st.to_dict(), st.__dict__)

    def testToDictWithArg(self):
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()

