import unittest

from dict_toolset import compare
from dict_toolset._compare import primitive_list_compare


class CompareTest(unittest.TestCase):

    def test_primitives(self):
        l1 = ["a", "b", "c", "c", "c"]
        l2 = ["a", "b", "c", "d"]

        result = list(primitive_list_compare(l1, l2, []))
        self.assertEqual(len(result), 3)

    def test_c1(self):
        result = list(compare({
            "name": "Supi",
            "sub": {
                "name": "SupiSub"
            }
        }, {
            "name": "Supi",
            "sub": {
                "name": "SupiSub",
                "content": "Sdjjahsdh"
            }
        }))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "MISSING sub.content IN A: Sdjjahsdh")

    def test_c2(self):
        result = list(compare({
            "name": "Supi",
            "subs": [
                "str"
            ]
        }, {
            "name": "Supi",
            "subs": [
                "duf",
                "str",
            ]
        }))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "MISSING")

    def test_c3(self):
        result = list(compare([
            {
                "id": "djajshd",
                "name": "supi",
                "kacki": "dsadasdasd"
            }
        ], [
            {
                "id": "sdajsjdhas",
                "name": "supi2",
                "kacki": "dsad2asdasdd"
            },
            {
                "id": "djajshd",
                "name": "supi",
                "kacki": "dsadasdasd"
            },
        ]))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "MISSING")

    def test_int_index(self):
        result = list(compare([
            {"name": "supi"}
        ], [
            {"name": "supi2"}
        ]))

        self.assertEqual(len(result), 1)
        self.assertEqual(str(result[0]), "NOT_EQUAL [0].name supi!=supi2")

    def test_uuid_index(self):
        result = list(compare([
            {"uuid": "123", "name": "supi"}
        ], [
            {"uuid": "123", "name": "supi2"}
        ]))

        self.assertEqual(len(result), 1)
        self.assertEqual(str(result[0]), "NOT_EQUAL [uuid=123].name supi!=supi2")