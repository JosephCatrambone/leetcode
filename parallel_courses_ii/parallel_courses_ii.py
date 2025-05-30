import itertools
from typing import List, Dict

class Solution:
	@staticmethod
	def get_min_course_depth(dependencies: Dict[int, set]) -> Dict[int, int]:
		"""
		Return a mapping of node id -> depth, with terminal nodes having depth 1.
		Returns the shortest path to the terminal node.
		We do a slightly inefficient stupid thing and repeatedly iterate over the items, rather than doing this
		recursively or using a stack because I'm lazy.
		Initialize all nodes to have a depth of HUGE_NUM, then set the terminals to depth 1.
		Iterate and set the depth of a node to be (smallest subsequent + 1).
		"""
		depth = dict()
		# Init to 'infinity'
		for k in dependencies.keys():
			depth[k] = 1000000
		# Set terminals to '1'.
		for k, deps in dependencies.items():
			if not deps:
				depth[k] = 1
		changed = True
		while changed:
			changed = False
			for cid, deps in dependencies.items():
				for d in deps:
					if depth[d]+1 < depth[cid]:
						depth[cid] = depth[d] + 1
						changed = True
		return depth

	@staticmethod
	def get_max_course_depth(dependencies: Dict[int, set]) -> Dict[int, int]:
		"""
		Return a mapping of node id -> depth, with terminal nodes having depth 1.
		Iterate to compute the dpeth of the deepest node.
		Rather than do the recursive approach which is slightly faster, we watch for changes to stop.
		"""
		depth = dict()
		for k in dependencies.keys():
			depth[k] = 1
		changed = True
		while changed:
			changed = False
			for cid, deps in dependencies.items():
				new_depth = depth[cid] + 1
				for dep in deps:
					old_depth = depth[dep]
					if new_depth > old_depth:
						depth[dep] = new_depth
						changed = True
		return depth

	@staticmethod
	def build_course_priority(dependencies: Dict[int, set]) -> Dict:
		"""Build a mapping from course ID to the number of unlocked courses."""
		priority = dict()
		# Give priority based on the number of immediate dependencies that are unlocked:
		# This is only a first-order dependency.  We should find the n-th order.
		for course, prereqs in dependencies.items():
			if course not in priority:
				priority[course] = 0
			for prereq in prereqs:
				if prereq not in priority:
					priority[prereq] = 0
				priority[prereq] += 0.0001  # DEBUG.  Set this to += 1 to use the number of unlocked as a priority.
		# Also add priority based on how deep this job goes.
		min_depths = Solution.get_min_course_depth(dependencies)
		max_depths = Solution.get_max_course_depth(dependencies)
		for course in dependencies.keys():
			priority[course] += min_depths[course]
			priority[course] += max_depths[course]
		return priority

	@staticmethod
	def build_graph(relation_list: List[List[int]], max_course_idx:int = 0) -> dict:
		"""
		relation_list starts as relation[course idx] = [previous_idx, next_idx].
		We want to remap this to dependencies[cource_id] = {set of required courses}
		"""
		dependencies = dict()
		for prev_idx, next_idx in relation_list:
			if prev_idx not in dependencies:
				dependencies[prev_idx] = set()
			if next_idx not in dependencies:
				dependencies[next_idx] = set()
			dependencies[next_idx].add(prev_idx)
		# If there are any unlisted elements, add them here:
		if max_course_idx > 0:
			for course_idx in range(1, max_course_idx):
				if course_idx not in dependencies:
					dependencies[course_idx] = set()
		return dependencies

	@staticmethod
	def yield_topological_sorts(
			dependencies: Dict[int, set],
			priority: Dict[int, int],
			courses_per_session: int,
			max_sessions: int = -1,
			sessions: List = None,
			brute_force: bool = False,  # Exhaustively iterate.
	) -> List[List[int]]:
		"""
		Iteratively generates all possible topological sorts, skipping those who would use more than max_sesions at courses_per_session to complete.
		Produces a set of semesters/sessions, each with fewer than courses_per_session.
		"""
		# Initialize, for the base case:
		if sessions is None:
			sessions = list()  # [[1, 2, 3], [5, 6], ...]
		courses_taken = set()
		for semester in sessions:
			for course_id in semester:
				courses_taken.add(course_id)
		courses_not_taken = set()
		for course_id in dependencies.keys():
			if course_id not in courses_taken:
				courses_not_taken.add(course_id)

		# Base case:
		if len(courses_not_taken) == 0:
			yield sessions  # Lesson plan available!
		else:
			# See what courses we can take.
			courses_available = list()  # Set instead of list because we may want to perform some pop/push.
			for course in courses_not_taken:
				if dependencies[course].issubset(courses_taken):  # All dependencies are satisfied!
					courses_available.append(course)

			if len(courses_available) > 0 and (max_sessions < 0 or len(sessions)+1 < max_sessions):
				# We have an unfortunate double-permutation now.  We can take courses_per_session of the courses_available.
				# For each combination there, try addnig those to the courses taken, push it onto the session list, and recurse.
				# We should consider sorting by the courses which open the most options.
				if len(courses_available) <= courses_per_session:
					# Just take all of the courses.
					yield from Solution.yield_topological_sorts(dependencies, priority, courses_per_session, max_sessions, sessions + [courses_available,])
				else:
					"""
					# Naive but functional solution tries to brute force the different options.
					for semester in itertools.combinations(courses_available, courses_per_session):
						# Temporarily add this semester as a poossible course of study.
						# Convert the semester object (a tuple) to a list.
						yield from Solution.yield_topological_sorts(dependencies, priority, courses_per_session, max_sessions, sessions + [list(semester), ])
					"""
					if brute_force:
						# Bounded pseudo-DFS which tries to cap
						# Pre-sort to get higher-priority options first.
						courses_available = sorted(courses_available, key=lambda cid: priority[cid], reverse=True)
						for semester in itertools.combinations(courses_available, courses_per_session):
							yield from Solution.yield_topological_sorts(dependencies, priority, courses_per_session, max_sessions, sessions + [list(semester), ])
					else:
						# Smarter solution tries to greedily take the courses which unlock the most items first.
						courses_available = sorted(courses_available, key=lambda cid: priority[cid], reverse=True)
						next_semester = courses_available[:courses_per_session]
						yield from Solution.yield_topological_sorts(dependencies, priority, courses_per_session, max_sessions, sessions + [next_semester, ])

	def minNumberOfSemesters(self, n: int, relations: List[List[int]], k: int) -> int:
		num_courses = n + 1
		max_courses_per_semester = k
		deps = Solution.build_graph(relations, num_courses)
		priority = Solution.build_course_priority(deps)
		plan = None
		fewest_semesters = 1
		"""
		# Brute force-ish:
		for lesson_plan in Solution.yield_topological_sorts(deps, priority, max_courses_per_semester):
			if plan is None or len(lesson_plan) < fewest_semesters:
				fewest_semesters = len(lesson_plan)
				plan = lesson_plan
		"""
		"""
		# Iterative deepening:
		while plan is None:
			for candidate_plan in Solution.yield_topological_sorts(deps, priority, max_courses_per_semester, max_sessions=fewest_semesters):
				if candidate_plan is not None:
					plan = candidate_plan
			if plan is None:
				fewest_semesters += 1
		fewest_semesters = len(plan)
		"""
		# First, fetch the greedy solution to see if we can get a ballpark:
		plan = next(Solution.yield_topological_sorts(deps, priority, max_courses_per_semester))
		fewest_semesters = len(plan)
		# If there exist any inefficiencies in the solution (i.e, there's a not-full semester for any but the last), then brute force around that.
		inefficiency = any([len(semester) < max_courses_per_semester for semester in plan])
		if inefficiency:
			for candidate_plan in Solution.yield_topological_sorts(deps, priority, max_courses_per_semester, max_sessions=fewest_semesters, brute_force=True):
				if len(candidate_plan) < fewest_semesters:
					plan = candidate_plan
					fewest_semesters = len(plan)

		#print(f"deps: {deps}")
		#print(f"priority: {priority}")
		#print(f"plan: {plan}")
		#print(f"fewest_semesters: {fewest_semesters}")
		return fewest_semesters
