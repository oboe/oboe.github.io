
### Generic

Where do you see yourself in 3 years?
```
I'd like to be an exceptional software engineer, go deeper, have even more mastery.
```
### Trivia

Why do you want to work for sp?
```
uni finance
```
Why is a generator in python?
```
Generator functions are functions that return generators objects. 

Created by using yields within your function to return values back to the caller. And when recalled the function resumes the function at it's last point it yielded and will continue. Until it eve

The key benefit being that you can easily create these objects that can be iterated on.

Function call, place it on the stack then on return it exits. For generators, function called, place it on stack then the returning generator iterator stores this stack. So it can be resumed later on.
```
What is an iterator in python?
```
Iterator objects, implement dunder methods iter and next. Can use in for loops. Next does returns and eventually throws StopIteration
```

What is the difference between a generator and iterator?
```
Generators objects implement iterators. So you can iterate on them.
Raise StopIteration when done.
Special type of iterator. Generates values on the fly one at a time. Can represent infinite sequences.

```
What is a decorator in python?
```
Modify functions or classes without changing source code.

Lets you wrap function/classes calls. It's straight up just a function that takes in a function object. And returns a new class/function object that works differently
```

How does mutability and immutability work in python?
```
immutable
- Cant be changed
- assignment creates new object
- hashable
mutable
- can be modified
- object change in place
```
How do args and kwargs work in python?
```
args tuple style function parameters

kwargs dictionary style function parameters

Starts at the front

```
How does a merge vs rebase work?
```
Merge, merges the branches

Rebase destroys feature branch and plants it onto mainline
```
What do dunder methods do?
```
special methods

init, name, iter, next, etc
```

How do you inherit from a class?

How do I implement a hash func for a class

### Qs
```
REGEX
\d Decimal -> \D
\s Space -> \S
\w Whatever -> \W

* 0 or more
+ 1 or more
? 0 or 1
{a,b} a or b

^ start
$ end

<https://docs.python.org/3/howto/regex.html>
```

```python
import re
import datetime

MONTH_MAP = {
        "F": 1,
        "G": 2,
        "H": 3,
        "J": 4,
        "K": 5,
        "M": 6,
        "N": 7,
        "Q": 8,
        "U": 9,
        "V": 10,
        "X": 11,
        "Z": 12
    }

def extract_date(code: str, date: datetime.date) -> datetime.date:
    match = re.match(r"^(\w+)(\D)([0-9]+)$", code)
    asset_code = match.group(1)
    month = MONTH_MAP[match.group(2)]
    year_suffix = match.group(3)
    print(f"{asset_code=} {month=} {year_suffix=}")
    year_prefix = int(str(date.year)[:-(len(year_suffix))])
    new_year = int(str(year_prefix) + year_suffix)
    ans = datetime.date(new_year, month, 1)
    if(ans > date):
        year_prefix += 1
        new_year = int(str(year_prefix) + year_suffix)
        ans = datetime.date(new_year,month,1)
    return ans

print(extract_date("GCM3", datetime.date(2021,1,1)))
print(extract_date("OF29", datetime.date(2021,1,1)))
print(extract_date("OF29", datetime.date(2031,1,1)))
print(extract_date("OG1", datetime.date(2021,2,1)))
```

<https://leetcode.com/problems/next-permutation/>
```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        last = nums[len(nums)-1]
        idx = len(nums)-1
        for i in reversed(range(len(nums))):
            if(last > nums[i]):
                idx = i
                break
            last = nums[i]
        
        next_idx = idx
        for i in range(idx+1, len(nums),1):
            print(i)
            if (nums[idx] >= nums[i]):
                break
            next_idx = i
        nums[idx], nums[next_idx] = nums[next_idx], nums[idx]

        
        if (idx+1 <= len(nums)-1):
            nums[idx+1:] = reversed(nums[idx+1:])
        if next_idx == idx:
            nums[:] = reversed(nums[:])
        
```

<https://leetcode.com/problems/multiply-strings/>
```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        ans = 0
        offset = 1
        for a in reversed(num1):
            total: str = ""
            carry = 0
            for b in reversed(num2):
                ab = int(a) * int(b)
                if carry:
                    ab += carry
                if ab >= 10:
                    carry = int(ab/10)
                    ab = ab%10
                else:
                    carry = 0
                total = str(ab) + total
            if carry:
                total = str(carry) + total
            ans += int(total) * offset
            offset *= 10
        return str(ans)

                
```

<https://leetcode.com/problems/string-to-integer-atoi/>
```python
class Solution:
    DIGITS = ["0","1","2","3","4","5","6","7","8","9"]
    def myAtoi(self, s: str) -> int:
        is_negative = False
        read_digits = False
        remaining = ""
        for c in s:
            if len(remaining) == 0:
                if c == " " and not read_digits:
                    continue
                elif c in self.DIGITS and c != "0":
                    remaining += c
                    read_digits = True
                elif c in self.DIGITS:
                    read_digits = True
                elif c == "-" and not is_negative and not read_digits:
                    read_digits = True
                    is_negative = True
                elif c == "+" and not is_negative and not read_digits:
                    read_digits = True
                    continue
                else:
                    break
            else:
                if c in self.DIGITS:
                    remaining += c
                else:
                    break
        if remaining == "":
            remaining = "0"
        ans = int(remaining) * -1 if is_negative else int(remaining)
        ans = max(ans, pow(-2,31))
        ans = min(ans, pow(2,31)-1)
        return ans
        
```