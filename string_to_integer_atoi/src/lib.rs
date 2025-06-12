pub struct Solution;

impl Solution {
	/// Convert the given string to a signed 32-bit integer.
	/// Ignores leading whitespace.
	/// Stops parsing at the first non-digit non-sign character.
	pub fn my_atoi(s: String) -> i32 {
		let mut started_parsing: bool = false;
		let mut negate = false;
		let mut accumulator: i32 = 0;
		for c in s.trim().chars().into_iter() {
			if c == '+' && !started_parsing {
				started_parsing = true;
			} else if c == '-' && !started_parsing {
				started_parsing = true;
				negate = true;
			} else if c.is_numeric() {
				started_parsing = true;
				// We can't use the same path for positive and negative because the saturation operation caps at different places.
				let digit = ((c as u8) & 0x0F) as i32;
				accumulator = accumulator.saturating_mul(10);
				if negate {
					accumulator = accumulator.saturating_sub_unsigned(digit as u32);
				} else {
					accumulator = accumulator.saturating_add(digit);
				}
			} else {
				break;
			}
		}
		accumulator
	}
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn case1() {
		let result = Solution::my_atoi("42".to_owned());
		assert_eq!(result, 42);
	}

	#[test]
	fn case2() {
		let result = Solution::my_atoi("-042".to_owned());
		assert_eq!(result, -42);
	}

	#[test]
	fn case3() {
		let result = Solution::my_atoi("1337c0d3".to_owned());
		assert_eq!(result, 1337);
	}

	#[test]
	fn case4() {
		let result = Solution::my_atoi("0-1".to_owned());
		assert_eq!(result, 0);
	}

	#[test]
	fn case5() {
		let result = Solution::my_atoi("words and 987".to_owned());
		assert_eq!(result, 0);
	}

	#[test]
	fn case_oob() {
		let result = Solution::my_atoi("2147483649".to_owned());
		assert_eq!(result, i32::MAX);
		let result = Solution::my_atoi("2147483647".to_owned());
		assert_eq!(result, i32::MAX);
		let result = Solution::my_atoi("-2147483649".to_owned());
		assert_eq!(result, i32::MIN);
		let result = Solution::my_atoi("-2147483650".to_owned());
		assert_eq!(result, i32::MIN);
	}
}
