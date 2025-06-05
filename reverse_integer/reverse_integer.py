INT_MIN = -2147483648
INT_MAX = 2147483647

def dumb_reverse(x: int):
    y = 0
    invert = False
    if x < 0:
        invert = True
        x = -x
    while x > 0:
        y *= 10
        y += x%10
        x //= 10
    if invert:
        y = -y
    
    # Bounds check:
    if y < INT_MIN:
        y = 0
    if y > INT_MAX:
        y = 0

    return y

class Solution:
    def reverse(self, x: int) -> int:
        return dumb_reverse(x)
