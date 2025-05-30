
from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
	def __init__(self, val=0, left=None, right=None):
		self.val = val
		self.left = left
		self.right = right
	
	def __str__(self):
		left = "_"
		right = "_"
		if self.left is not None:
			left = self.left.__str__()
		if self.right is not None:
			right = self.right.__str__()
		return f"[{self.val} ({left}) ({right})]"
	
	@classmethod
	def from_array(cls, arr):
		nodes = list()
		get_left_child_idx = lambda x: x*2+1
		get_right_child_idx = lambda x: (x+1)*2
		for num in arr:
			if num is not None:
				nodes.append(TreeNode(val=num, left=None, right=None))
			else:
				nodes.append(None)
		for idx, node in enumerate(nodes):
			if node is None:
				continue
			left_child_idx = get_left_child_idx(idx)
			if left_child_idx < len(nodes):
				node.left = nodes[left_child_idx]
			right_child_idx = get_right_child_idx(idx)
			if right_child_idx < len(nodes):
				node.right = nodes[right_child_idx]
		return nodes[0]  # Root


def pseudo_palindromic_paths(root: Optional[TreeNode], depth = 0, digit_count_so_far: List[int] = None) -> int:
		# If we're just starting, make a list that maps each integer from 0 to 10 to 
		if digit_count_so_far is None:
			digit_count_so_far = list()
			for _ in range(0, 10):
				digit_count_so_far.append(0)
		digit_count_so_far[root.val] += 1
		# If we are at the end of the tree and the digits so far is a pseudo-palindromic, return it, otherwise return the sum of the children.
		if root.left is None and root.right is None:
			# There can be exactly one odd digit in the palindrome count.
			num_odds = 0
			for count in digit_count_so_far:
				if count % 2 == 1:
					num_odds += 1
			digit_count_so_far[root.val] -= 1 # Pop this digit as we move up.
			if num_odds == ((depth+1) % 2):
				return 1
			else:
				return 0
		else:
			left_count = 0
			if root.left is not None:
				left_count = pseudo_palindromic_paths(root.left, depth+1, digit_count_so_far)
			right_count = 0
			if root.right is not None:
				right_count = pseudo_palindromic_paths(root.right, depth+1, digit_count_so_far)
			digit_count_so_far[root.val] -= 1 # Pop this digit as we move up.
			return left_count + right_count


class Solution:
	def pseudoPalindromicPaths (self, root: Optional[TreeNode]) -> int:
		return pseudo_palindromic_paths(root)
