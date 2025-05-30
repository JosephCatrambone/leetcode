def binsearch(value: int, nums: list[int], left: int | None = None, right: int | None = None) -> int | None:
	# Used for binary_search_twosum.
	# Binary search the numbers list.
	# O(log n) to find a value.
	if left is None:
		left = 0
	if right is None:
		right = len(nums)-1

	if left >= right:
		if 0 <= left < len(nums) and nums[left] == value:
			return left
		else:
			return None
	else:
		midpoint = (left+right)//2
		index = binsearch(value, nums, left, midpoint)
		if index is not None:
			return index
		index = binsearch(value, nums, midpoint+1, right)
		return index

def hash_search_twosum(nums: list[int], target: int) -> list[int]:
	# Total runtime: O(n)
	# Total memory: O(n^2)
	# tl;dr: Use a hashmap with O(1) lookup to map to their indices and counts.
	num_to_index = dict()
	for idx, n in enumerate(nums):
		if n not in num_to_index:
			num_to_index[n] = list()
		num_to_index[n].append(idx)
	for n in nums:
		if (target - n) in num_to_index:
			# Single special case where we have two copies of the same number.
			first_index = num_to_index[n][0]
			second_index = num_to_index[target-n][-1]
			if first_index != second_index:
				return [first_index, second_index]

def binary_search_twosum(nums: list[int], target: int) -> list[int]:
	# Total runtime: O(n log n)
	# Total memory: O(n)
	# tl;dr: Sort the list to have an easier time finding pairs.
	# O(n log n) to sort the list, then O(n) * O(log n) searches.
	# See the other solutions.
	sorted_nums = sorted(nums)  # O(nlogn)
	
	for i in range(0, len(sorted_nums)): # O(n)
		# Search the rest of the list from i to the end for target-i.
		j = binsearch(target-sorted_nums[i], sorted_nums, i+1)  # O(log n)
		if j is None:
			continue
		if sorted_nums[i] + sorted_nums[j] == target:
			# Do a search for the original sorted_nums[i] to return that index.
			# One-time O(n)
			remapped_i = nums.index(sorted_nums[i])
			for remapped_j in range(remapped_i+1, len(nums)):
				if nums[remapped_j] == sorted_nums[j]:
					return [remapped_i, remapped_j]
	print("Unreachable")

def naive_twosum(nums: list[int], target: int) -> list[int]:
	# Total runtime: O(n^2)
	# Total memory: O(n)
	for i in range(0, len(nums)):
		for j in range(i+1, len(nums)):
			if nums[i]+nums[j] == target:
				return [i, j]

class Solution:
	# Total runtime: O(n log n)
	# Total memory: O(n)
	def twoSum(self, nums: List[int], target: int) -> List[int]:
		return hash_search_twosum(nums, target)

