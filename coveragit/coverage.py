from xml.dom import minidom
from os import getcwd, path
from coveragit import ContextualizedException
import re


class CoverageProcessorException(ContextualizedException):
    pass


class NoSuchCoverageException(CoverageProcessorException):
    def __init__(self, xml_path):
        context = {'xml_path': xml_path}
        CoverageProcessorException.__init__(self, 'No such coverage .xml file', context)


class InvalidCoverageException(CoverageProcessorException):
    def __init__(self, xml_path, previous_exception):
        context = {'xml_path': xml_path}
        CoverageProcessorException.__init__(self, 'Invalid coverage .xml file', context, previous_exception)


class CoverageProcessor(object):
    @staticmethod
    def _get_uncovered_code(xml_path):
        if not path.isfile(xml_path):
            raise NoSuchCoverageException(xml_path)

        try:
            xml_doc = minidom.parse(xml_path)

            files_dom = xml_doc.getElementsByTagName('file')

            uncovered_code = {}
            for file_dom in files_dom:
                uncovered_lines = []

                lines_dom = file_dom.getElementsByTagName('line')
                for line_dom in lines_dom:
                    count = int(line_dom.attributes['count'].value)
                    line_number = int(line_dom.attributes['num'].value)
                    if count == 0:
                        uncovered_lines.append(line_number)

                if uncovered_lines:
                    cwd = getcwd().rstrip('/') + '/'
                    file_name = file_dom.attributes['name'].value
                    file_name = re.sub('^%s' % cwd, '', file_name)
                    uncovered_code[file_name] = uncovered_lines

            return uncovered_code
        except Exception as e:
            raise InvalidCoverageException(xml_path, e)

    def get_missing_coverage(self, additions, xml_path):
        uncovered_code = self._get_uncovered_code(xml_path)
        missing_coverage = {}

        relevant_files = list(set(uncovered_code) & set(additions))

        for file_name in relevant_files:
            uncovered_lines = uncovered_code[file_name]
            relevant_lines = additions[file_name]
            uncovered_relevant_lines = list(set(uncovered_lines) & set(relevant_lines))
            if uncovered_relevant_lines:
                missing_coverage[file_name] = uncovered_relevant_lines

        return missing_coverage
