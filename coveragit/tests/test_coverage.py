from unittest import TestCase
from coveragit.coverage import CoverageProcessor, NoSuchCoverageException, InvalidCoverageException
import os


class TestCoverage(TestCase):
    def setUp(self):
        self._coverage_processor = CoverageProcessor()

    def test_xml_not_found(self):
        additions = {}
        xml_path = 'not/found/path.xml'

        self.assertRaises(
            NoSuchCoverageException,
            self._coverage_processor.get_missing_coverage,
            additions,
            xml_path
        )

    def test_get_missing_coverage(self):
        additions = {
            '/foo/bar/hello/world.php': [3, 23, 25, 29],
            '/foo/bar/hello/xxx.php': [1, 2, 3]
        }
        xml_path = '{base_path}/fixtures/coverage.xml'.format(base_path=os.path.dirname(os.path.realpath(__file__)))

        missing_coverage = self._coverage_processor.get_missing_coverage(additions, xml_path)
        self.assertEqual(1, len(missing_coverage))
        self.assertEqual(2, len(missing_coverage['/foo/bar/hello/world.php']))
        self.assertIn(25, missing_coverage['/foo/bar/hello/world.php'])
        self.assertIn(23, missing_coverage['/foo/bar/hello/world.php'])

    def test_invalid_xml(self):
        additions = {}
        xml_path = '{base_path}/fixtures/invalid_coverage.xml'.format(base_path=os.path.dirname(os.path.realpath(__file__)))

        self.assertRaises(
            InvalidCoverageException,
            self._coverage_processor.get_missing_coverage,
            additions,
            xml_path
        )
