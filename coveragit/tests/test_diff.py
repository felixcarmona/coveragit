from unittest import TestCase
from coveragit.diff import AdditionsFinder
import os


class TestDiff(TestCase):
    def test_get_additions(self):
        additions_finder = AdditionsFinder()

        repository_path = '{base_path}/fixtures/repository'.format(
            base_path=os.path.dirname(os.path.realpath(__file__)))

        additions = additions_finder.get_additions_for_base('master', repository_path)

        expected_additions = {
            'test_a': [9, 17, 18, 19, 28],
            'test_b': [4, 5, 11],
            'test_d': [1, 2, 3, 4, 5]
        }

        self.assertEqual(len(expected_additions), len(additions))
        self._assert_unordered_lists_equals(additions['test_a'], expected_additions['test_a'])
        self._assert_unordered_lists_equals(additions['test_b'], expected_additions['test_b'])
        self._assert_unordered_lists_equals(additions['test_d'], expected_additions['test_d'])

    def _assert_unordered_lists_equals(self, list_one, list_two):
        self.assertTrue(len(list_one) == len(list_two) and sorted(list_one) == sorted(list_two))
