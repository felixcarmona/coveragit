import sys
import argparse
from coveragit.coverage import CoverageProcessor
from coveragit.diff import AdditionsFinder
from coveragit.application.console.display import Display


class Application:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Check the uncovered code lines which have been modified or added in an specific pull request or commit')
        parser.add_argument('--base', '-b', type=str, default='HEAD~1',
                            help='Base branch, tag, commit, or history marker to compare the current revision')
        parser.add_argument('--concise', '-c', action='store_true', help='Only display the affected uncovered lines')
        parser.add_argument('--xml', '-x', type=str, default='coverage.xml', help='Path of the generated coverage .xml')
        parser.add_argument('--silently', '-s', action='store_true',
                            help='Even with missing coverage, exit with success system exit status')
        parser.set_defaults(concise=False)

        args = parser.parse_args()

        self._additions_finder = AdditionsFinder()
        self._coverage_processor = CoverageProcessor()
        self._base = args.base
        self._xml = args.xml
        self._concise = args.concise
        self._silently = args.silently

    def run(self):
        try:
            additions = self._additions_finder.get_additions_for_base(self._base)
            missing_coverage = self._coverage_processor.get_missing_coverage(additions, self._xml)

            if missing_coverage:
                visualizer = Display()
                visualizer.display_missing_coverage(missing_coverage, self._concise)
                if not self._silently:
                    sys.exit(2)
            else:
                print('\033[32m100% relevant lines covered\033[m')
        except Exception as e:
            print("\033[31m %s\033[m" % e.message)
            sys.exit(2)
