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
                "str",
                "duf"
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
                "id": "djajshd",
                "name": "supi",
                "kacki": "dsadasdasd"
            },
            {
                "id": "sdajsjdhas",
                "name": "supi2",
                "kacki": "dsad2asdasdd"
            },
        ]))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "MISSING")
