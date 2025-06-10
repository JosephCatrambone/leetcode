
# Quick and simple 2D container.
class WordGrid:
    def __init__(self, width: int, height: int):
        self.data = list()
        for i in range(width*height):
            self.data.append(None)
        self.width = width
        self.height = height
    def _check_bounds(self, x, y):
        if x < 0 or x >= self.width:
            raise Exception(f"X {x} oob: width is {self.width}")
        if y < 0 or y >= self.height:
            raise Exception(f"Y {y} is oob: height is {self.height}")
    def set(self, x: int, y: int, value: str):
        self._check_bounds(x, y)
        self.data[x + (y*self.width)] = value
    def get(self, x: int, y: int) -> str:
        self._check_bounds(x, y)
        return self.data[x + (y*self.width)]

def naive(s: str, num_rows: int) -> str:
    # Early out:
    if num_rows == 1:
        return s

    # Do the obvious and dumb thing: allocate a grid and fill letters.

    # Fill a zig-zag pattern:
    grid = WordGrid(len(s), num_rows)
    x = 0
    y = 0
    dx = 0
    dy = 1
    for c in s:
        grid.set(x, y, c)
        x += dx
        y += dy
        if y >= grid.height-1:
            dx = 1
            dy = -1
        elif y == 0:
            dx = 0
            dy = 1

    # Read back a zigzag pattern.
    out = ""
    for y in range(0, grid.height):
        for x in range(0, grid.width):
            c = grid.get(x, y)
            if c is not None:
                out += c
    return out
    

class Solution:
    def convert(self, s: str, numRows: int) -> str:
        return naive(s, numRows)

if __name__ == "__main__":
    test_cases = [
        (("PAYPALISHIRING", 3), "PAHNAPLSIIGYIR"),
        (("PAYPALISHIRING", 4), "PINALSIGYAHRPI"),
        (("A", 1), "A"),
        (("AB", 1), "AB"),
        (("ABC", 2), "ACB"),
        (("ABCD", 2), "ACBD"),
    ]

    s = Solution()
    for test_in, expected_out in test_cases:
        prog_out = s.convert(*test_in)
        if prog_out != expected_out:
            print(f"FAIL: expected {expected_out} but got {prog_out}")
        else:
            print("PASS")
