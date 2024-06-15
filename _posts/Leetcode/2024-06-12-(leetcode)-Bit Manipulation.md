## Context
Working out a negative of a number
- Invert all bits and increase number by one

Fast odd, even check
- x & 1

Operations
- & and
- | or
- ^ xor
- ~ not
- x << k (bit shifts) (multiply by 2^k)
- edit specific bits with & (1<<k)

Functions
```
__buildin_popcount(x) number of ones
__buildin_parity(x) parity, even or odd number of ones
__buildin_clz(x) number of zero at start
__buildin_ctz(x) number of zero at end
```

## Qs
<https://leetcode.com/problems/single-number>
Naive
- xor will cancel out all duplicate 1s

```cpp
class Solution {
public:
    int singleNumber(vector<int>& nums) {
        int val = 0;
        for(int i : nums){
            val = val ^ i;
        }
        return val;
    }
};
```
<https://leetcode.com/problems/number-of-1-bits>

```cpp
class Solution {
public:
    int hammingWeight(uint32_t n) {
        int count = 0;
        for(int i = 0; i < 32 ; i++){
            int j = (1<<i);
            if (n&j){
                count++;
            }
        }
        return count;
    }
};
```

<https://leetcode.com/problems/counting-bits>
```cpp
class Solution {
public:
    vector<int> countBits(int n) {
        vector<int> ans;
        for(int i = 0 ; i <= n ;i++){
            int ones = 0;
            for(int k = 0 ; k <= 31 ; k++){
                if(i & (1<<k)) ones++;
            }
            ans.push_back(ones);
        }
        return ans;
    }
};
```

<https://leetcode.com/problems/reverse-bits>
Naive
- go bit by bit adding it to the new number

```cpp
class Solution {
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t ans = 0;
        for(int i = 0 ; i < 32 ;i++){
            if(n&(1<<i)){
                ans = ans | (1<<(31-i));
            }
        }
        return ans;
    }
};
```

<https://leetcode.com/problems/missing-number>
Naive
- nlogn, sort and pass
- I know the size and what numbers are in the 
- so could 1 pass xor get num, then xor pass list and get remaining num

```cpp
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int ans = 0;
        for(int i = 0 ;i <= nums.size() ;i++){
            ans ^= i;
        }
        for(int i = 0 ;i < nums.size() ;i++){
            ans ^= nums[i];
        }
        return ans;
    }
};
```

<https://leetcode.com/problems/sum-of-two-integers>

```cpp
class Solution {
public:
    int getSum(int a, int b) {
        return(b==0) ? a : getSum(a^b,(a&b)<<1);
    }
};
```

<https://leetcode.com/problems/reverse-integer>
Naive
- cheating just convert it into a string

```cpp
class Solution {
public:
    int reverse(int x) {
        bool negative = false;
        long long l = x;
        if (x < 0) {negative=true; l*=-1;}
        string s = to_string(l);
        std::reverse(s.begin(), s.end());
        if(negative) s = "-" + s;
        try{
            return stoi(s);
        } catch(const std::out_of_range e) {
            return 0;
        }
    }
};
```
