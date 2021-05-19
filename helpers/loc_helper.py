import os


class LOCHelper:

    def __init__(self):
        pass

    """
    Inspired by this stackoverflow post.
    https://stackoverflow.com/questions/38543709/count-lines-of-code-in-directory-using-python
    Counts lines of code excluding comments.
    """

    def countlines(self, rootdir, total_lines=0, header=True, begin_start=None,
                   code_only=True):

        def _get_new_lines(source):
            total = len(source)
            i = 0
            while i < len(source):
                line = source[i]
                trimline = line.lstrip(" ")

                if trimline.startswith('#') or trimline == '':
                    total -= 1
                elif '"""' in trimline:  # docstring begin
                    if trimline.count('"""') == 2:  # docstring end on same line
                        total -= 1
                        i += 1
                        continue
                    doc_start = i
                    i += 1
                    while '"""' not in source[i]:  # docstring end
                        i += 1
                    doc_end = i
                    total -= (doc_end - doc_start + 1)
                i += 1
            return total

        for name in os.listdir(rootdir):
            file = os.path.join(rootdir, name)
            if os.path.isfile(file) and file.endswith('.py'):
                with open(file, 'r') as f:
                    source = f.readlines()

                if code_only:
                    new_lines = _get_new_lines(source)
                else:
                    new_lines = len(source)
                total_lines += new_lines

        for file in os.listdir(rootdir):
            file = os.path.join(rootdir, file)
            if os.path.isdir(file):
                total_lines = self.countlines(file, total_lines, header=False,
                                              begin_start=rootdir, code_only=code_only)
        return total_lines
