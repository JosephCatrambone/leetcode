
def median_naive(nums1: list[int], nums2: list[int]) -> float:
    # O(n log n)
    new_arr = sorted(nums1 + nums2)
    if len(new_arr) % 2 == 1:
        # Odd length. We have a middle.
        return new_arr[len(new_arr)//2]
    else:
        return (new_arr[len(new_arr)//2 - 1] + new_arr[(len(new_arr)//2)]) / 2.0


def find_median_sorted(nums: list[int]) -> tuple[int, float]:
    # O(1)
    # Returns the index after which the median would appear and the value of the median.
    # Assumes nums is a sorted list.
    if len(nums) % 2 == 1:
        # Odd length. We have a middle.
        index = len(nums)//2
        return index, nums[index]
    else:
        index = len(nums)//2 - 1
        return index, (nums[index] + nums[index+1]) / 2.0
    

def seek_median(nums1: list[int], nums2: list[int]) -> float:
    # TODO: This is still O(nlogn)  Need to get it down to O(logn)
    return find_median_sorted(sorted(nums1 + nums2))[1]
    

class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        return seek_median(nums1, nums2)
        #return median_naive(nums1, nums2)


def main():
    import random
    s = Solution()
    canned_tests = [
            (([1, 3], [2,]), 2),
            (([1, 2], [3, 4]), 2.5),
            (([1, 3, 5], [9, 11]), 5),
            (([1, 3, 5], [9, 11, 13]), 7),
            (([1,], [9, 11, 13]), 10),
    ]
    
    generated_tests = list()
    for _ in range(50):
        a = list()
        b = list()
        for i in range(-1000, 1000):
            if random.random() > 0.8:
                a.append(i)
            if random.random() > 0.8:
                b.append(i)
        generated_tests.append(((a, b), median_naive(a, b)))

    test_cases = canned_tests + generated_tests
    
    for test_input, expected_output in test_cases:
        out = s.findMedianSortedArrays(*test_input)
        if out != expected_output:
            print(f"FAILURE: expected {expected_output} but got {out}")
        else:
            print("PASS")

if __name__=="__main__":
    main()
