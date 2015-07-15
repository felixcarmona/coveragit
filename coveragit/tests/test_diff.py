from unittest import TestCase
from coveragit.diff import AdditionsFinder
import os
from subprocess import Popen, PIPE
from random import randint
from shutil import copy
from os import remove
from glob import glob


class TestDiff(TestCase):
    def setUp(self):
        self._build_path = '{base_path}/fixtures/build/{directory}'.format(
            base_path=os.path.dirname(os.path.realpath(__file__)),
            directory=randint(0, 9999999999)
        )

        self._create_build_path()
        self._init_repository()
        self._apply_commit(1)
        self._create_branch('develop')
        self._apply_commit(2)
        self._apply_commit(3)

    def test(self):
        additions_finder = AdditionsFinder()

        additions = additions_finder.get_additions_for_base('master', self._build_path)

        expected_additions = {
            'test_d': [1, 2, 3, 4, 5, 6, 7],
            'test_a': [24, 19, 20, 11, 12, 5]
        }

        self.assertEqual(len(expected_additions), len(additions))
        self._assert_unordered_lists_equals(additions['test_a'], expected_additions['test_a'])
        self._assert_unordered_lists_equals(additions['test_d'], expected_additions['test_d'])

    def tearDown(self):
        command = ['rm', '-rf', self._build_path]
        Popen(command, stdout=PIPE).communicate()

    def _assert_unordered_lists_equals(self, list_one, list_two):
        self.assertTrue(len(list_one) == len(list_two) and sorted(list_one) == sorted(list_two))

    def _apply_commit(self, number):
        commit_path = '{base_path}/fixtures/repository_history/commit_{number}/'.format(
            base_path=os.path.dirname(os.path.realpath(__file__)),
            number=number
        )

        for filename in glob(os.path.join(self._build_path, '*')):
            remove(filename)

        for filename in glob(os.path.join(commit_path, '*')):
            copy(
                filename,
                self._build_path
            )

        command = ['git', 'add', '.']
        Popen(command, cwd=self._build_path, stdout=PIPE).communicate()

        command = ['git', 'commit', '-m', '{number}'.format(number=number)]
        Popen(command, cwd=self._build_path, stdout=PIPE).communicate()

    def _create_branch(self, name):
        command = ['git', 'checkout', '-b', '{name}'.format(name=name)]
        Popen(command, cwd=self._build_path, stdout=PIPE, stderr=PIPE).communicate()

    def _init_repository(self):
        command = ['git', 'init']
        Popen(command, cwd=self._build_path, stdout=PIPE).communicate()

    def _create_build_path(self):
        command = ['mkdir', self._build_path]
        Popen(command, stdout=PIPE).communicate()
