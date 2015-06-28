from os import popen
import re


class AdditionsFinder(object):
    @staticmethod
    def get_additions_for_base(base):
        additions = {}

        raw_diff = popen("git diff %s --unified=0" % base).read().strip()
        raw_diff_files = re.split('\ndiff', raw_diff)
        raw_diff_files = filter(None, raw_diff_files)  # remove empty elements from list

        for raw_diff_file in raw_diff_files:
            file_name_matches = re.findall(r'\nindex .*\n.*\n\+\+\+ b/(.*)\n', raw_diff_file, re.MULTILINE)

            # /dev/null matches
            if len(file_name_matches) == 0:
                continue

            file_name = file_name_matches[0]
            additions[file_name] = []
            chunks = re.findall(r'^@@ .* \+(.*[^,0]) @@', raw_diff_file, re.MULTILINE)
            for chunk in reversed(chunks):
                lines_range = chunk.split(',')
                if len(lines_range) == 2:
                    additions[file_name] += range(int(lines_range[0]), int(lines_range[0]) + int(lines_range[1]))
                else:
                    additions[file_name].append(int(lines_range[0]))

        return additions