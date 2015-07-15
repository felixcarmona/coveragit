from itertools import groupby
from operator import itemgetter


class Display(object):
    @staticmethod
    def _add_graceful_extra_lines(lines):
        for line in lines:
            if line + 1 not in lines and line + 2 in lines:
                lines.append(line + 1)

        return lines

    @staticmethod
    def _split_chunks(lines):
        lines = sorted(lines)
        result = []
        for k, g in groupby(enumerate(lines), lambda ix: ix[0] - ix[1]):
            result.append(map(itemgetter(1), g))

        return result

    def _add_extra_lines(self, line_numbers, file_lines_size):
        result = []
        for line_number in line_numbers:
            if line_number - 1 not in result:
                result.append(line_number - 1)

            if line_number not in result:
                result.append(line_number)

            if line_number + 1 not in result:
                result.append(line_number + 1)

        result = [line_number for line_number in result if 1 <= line_number <= file_lines_size]

        result = self._add_graceful_extra_lines(result)

        return result

    def display_missing_coverage(self, missing_coverage, is_concise):
        for file_name in missing_coverage:
            print("\033[41m\033[37m %s \033[m" % file_name)

            file_lines = [''] + [file_line.rstrip() for file_line in
                                 open(file_name)]  # [''] + because lists are zero-based

            uncovered_lines = missing_coverage[file_name]
            displayable_lines = self._add_extra_lines(uncovered_lines, len(file_lines) - 1)
            last_line = max(displayable_lines)
            chunks = self._split_chunks(displayable_lines)

            i = 1
            for chunk in chunks:
                for line in chunk:
                    line_zerofill = str(line).zfill(len("%s" % last_line))
                    if line in uncovered_lines:
                        print("%s: \033[31m%s\033[m" % (line_zerofill, file_lines[line]))
                    elif not is_concise:
                        print("%s: %s" % (line_zerofill, file_lines[line]))
                if not is_concise and i < len(chunks):
                    print("\033[36m-----------------------------------------\033[m")
                i += 1

            print("")
