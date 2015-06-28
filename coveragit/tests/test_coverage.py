from unittest import TestCase
from coveragit.coverage import CoverageProcessor, CoverageProcessorException


class TestCoverage(TestCase):
    def setUp(self):
        self._coverage_processor = CoverageProcessor()

    def test_xml_not_found(self):
        additions = []
        xml_path = 'not/found/path.xml'

        self.assertRaises(
            CoverageProcessorException,
            self._coverage_processor.get_missing_coverage,
            additions,
            xml_path
        )