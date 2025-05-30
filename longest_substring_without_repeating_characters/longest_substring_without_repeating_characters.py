import time

#
# NAIVE SOLUTION: Mostly for sanity checking.  Runs in O(n^2) or worse.
# 
def naive_lswr(s: str) -> int:
	# Linear memory.
	# O(n^2) runtime at least.  The set operation could make this O(n^3)
	longest_set_len = 0
	for i in range(0, len(s)):
		for j in range(i, len(s)+1):
			substring = s[i:j]
			candidate_substr_len = j-i
			if len(set(substring)) == candidate_substr_len:
				# All unique.
				if candidate_substr_len > longest_set_len:
					longest_set_len = candidate_substr_len
	return longest_set_len

#
# Scan Solution:
# 

def lswr_scan(s: str) -> int:
	# Start by scanning across the string to find the trivial window size.

	unique_chars = set()
	longest_unique_span_length = 0
	for idx, c in enumerate(s):
		if c not in unique_chars:
			unique_chars.add(c)
			unique_span_length = len(unique_chars)
			if unique_span_length > longest_unique_span_length:
				longest_unique_span = unique_span_length
		else:
			unique_chars = set()
			unique_chars.add(c)

	# Now we have to run past again to see if we can find a span longer than this.
	candidate_longest_span_length = longest_unique_span_length+1
	found_longer_span = True
	while found_longer_span:
		found_longer_span = False
		for idx in range(0, 1+len(s)-candidate_longest_span_length):  # We should seek right to the conflicts and backtrack.
			# If this span is unique...
			if len(set(s[idx:idx+candidate_longest_span_length])) == candidate_longest_span_length:
				found_longer_span = True
				longest_unique_span_length = candidate_longest_span_length
				candidate_longest_span_length += 1
			if found_longer_span:
				break
	return longest_unique_span_length
			
	
def lswr(s: str) -> set:
	# Note: substring, not subsequence.
	
	# At each point, we have a decision to make:
	# Add the current character to the longest subsequence (if possible)
	# End the longest subsequence and start a new one.
	# This screams 'dynamic programming' to me.
	
	# Every step we make a decision: add this character or don't.
	# If we add, the 'in progress' substring increases.
	# If we don't, we start a new 'in progress' subsequence.

	longest_set = set()
	candidate_set = set()
	#adding_to_longest_set = True
	#in_progress_sequences = list()

	for idx, c in enumerate(s):
		if c in candidate_set:
			# We can't take it.
			if len(candidate_set) > len(longest_set):
				longest_set = candidate_set
			candidate_set = set()
		candidate_set.add(c)
	# Do one last eval to see if the candidate is longer.
	if len(candidate_set) > len(longest_set):
		longest_set = candidate_set
	return longest_set

#
# Pivot/Merge Solution:
# 

class CharBucket:
	def __init__(self, s:str, start: int, end: int, left_child_ref = None, right_child_ref = None):
		self.s = s
		self.unique_characters = set(s[start:end])
		self.start = start
		self.end = end
		self.char_to_index = dict()
		for idx in range(start, end):
			self.char_to_index[s[idx]] = idx
		self.left_child = left_child_ref
		self.right_child = right_child_ref

	def can_merge_trivially(self, other) -> bool:
		# Returns true if these do not have any unique characters in common AND they are adjacent.
		return len(self.unique_characters.intersection(other.unique_characters)) == 0 and \
			(self.end == other.start or self.start == other.end)

	def can_merge_with_split(self, other) -> bool:
		# Returns true if we share a start or end and at most one overlapping character.
		return (self.end == other.start or self.start == other.end) and \
			len(self.unique_characters.intersection(other.unique_characters)) < 2

def lswr_pivots(s: str) -> int:
	# What if we borrow from Huffman coding and compression and build a list of prefixes?
	# The highest entropy substring would be the one with the most unique characters?
	# No, because we could have 'aaabcdaaa' and the max coding 'abcd' would get lost in the low-entropy 'a's.

	# What if we narrow down our search and flag the points where we have potential pivots?
	# Example: abcabc would have a pivot at the second 'a' because we've seen the character before?
	# Then instead of brute forcing span combos we can check which subspans are...
	# No, because 'abcdabcd'*1000 would have an evenly distributed count of pivots but 'abcd' is the max.
	# The O(n^2) solution is too long, time-wise, so we can't use anything dynamic programming.
	# We need to do O(n log n) worst case, so perhaps we need a bottom up or top-down merge system?

	# Could we do something like invert a trie?  Build and merge a bunch of prefix trees?
	# Can we prove that a greedy solution will work?
	pass

#
# Boilerplate and Tests:
# 

class Solution:
	def lengthOfLongestSubstring(self, s: str) -> int:
		#return lswr_pivots(s)
		return lswr_scan(s)
		#return naive_lswr(s)
		#return lswr(s)

def main():
	s = Solution()
	test_cases = [
			("abcabcbb", 3),
			("bbbbb", 1),
			("pwwkew", 3),
			("dvdf", 3),
			(" ", 1),
			("au", 2),
			("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "*10000, 95)
	]
	for input_data, expected_output in test_cases:
		start = time.time()
		out = s.lengthOfLongestSubstring(input_data)
		end = time.time()
		if expected_output != out:
			print(f"Failure ({end-start} sec):\nInput: {input_data}\nExpected Output: {expected_output}\nActual Output:{out}")
		else:
			print(f"Pass ({end-start} sec)")

if __name__ == "__main__":
	main()

