import io


class LineStream:
    def __init__(self, stream: io.TextIOBase):
        self.stream = stream

    def next_line(self) -> str:
        line = self.stream.readline()
        line = line.split("#")[0]
        return line.strip()

    def parse_ints(self, n: int, string: str, n_opt=0) -> tuple[int, ...]:
        """
        Read n integers from a string (n_opt optional).
        :param n: number of integers to read
        :param string: the string to read from
        :param n_opt: number of optional integers
        :return: a tuple of n integers
        """
        try:
            ii = tuple(map(int, string.split()))
        except ValueError:
            raise ValueError(f"Expected {n} integers in line: {string}")

        if not n - n_opt <= len(ii) <= n:
            raise ValueError(f"Expected {n} integers ({n_opt} optional) in line: {string}")

        return ii

    def next_ints(self, n: int, n_opt=0) -> tuple[int, ...]:
        line = self.next_line()
        return self.parse_ints(n, line, n_opt)

    def peek(self) -> str:
        """Return the next line without consuming it."""
        pos = self.stream.tell()
        line = self.stream.readline()
        self.stream.seek(pos)
        return line.strip()
