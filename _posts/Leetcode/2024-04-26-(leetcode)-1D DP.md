## Context
Use it when you want to
1. Find an optimal solution
2. Count the number of solutions

To solve DP, find the recursive function, what sub problems can you solve to calculate the answer to your problem?

The key of DP is to use memoization to cache the sub problem values efficiently.

This is why theres two ways of doing DP problems, top down or bottom up. Are you going down or up the recursive tree?


## Qs

<https://leetcode.com/problems/climbing-stairs>
Naive
- n=1 then 1 step 
- n=2 then 2 ways
- n=3 then 111,12,21


```cpp
class Solution {
public:
    int climbStairs(int n) {
        vector<int> v(n+2);
        v[0] = 1;
        for(int i = 0 ; i < n ;i++){
            v[i+1] += v[i];
            v[i+2] += v[i];
        }
        return v[n];
    }
};
```

<https://leetcode.com/problems/min-cost-climbing-stairs>
Naive
- min cost to reach the top of the floor
- cost(i) = min(cost(i-1),cost(i-2)) + value(i)
- start at step 0 or step 1

good
 - bottom up DP

```cpp
class Solution {
public:
    int minCostClimbingStairs(vector<int>& cost) {
        vector<int> fullCost(cost.size() + 2,INT_MAX);
        //start at 0 or 1
        fullCost[0] = 0;
        fullCost[1] = 0;
        for(int i = 0 ;i < cost.size() ;i++){
            fullCost[i+1] = min(fullCost[i+1], fullCost[i] + cost[i]);
            fullCost[i+2] = min(fullCost[i+2], fullCost[i] + cost[i]);
        }
        return fullCost[cost.size()];
    }
};
```

<https://leetcode.com/problems/house-robber>
Naive
- adjacent houses will trigger an alarm
- Return max amount of money you can rob without alerting the police

Good
- money(i) = max(money(i-2) + curr(i), money(i-1))

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        vector<int> ans(nums.size()+2,0);
        for(int i = 0 ; i < nums.size();i++){
            ans[i+1] = max(ans[i+1], ans[i]);
            ans[i+2] = max(ans[i+2], ans[i] + nums[i]);
        }
        int best = 0;
        for(int i = 0 ; i < nums.size();i++){
            ans[i] += nums[i];
            best = max(best,ans[i]);
        }
        return best;
    }
};
```

<https://leetcode.com/problems/house-robber-ii>
Naive
- Circular version now
- It's the same recursive relation but we need to handle the 
- i+1 to n
- and i to n-1

Good
- Just do it twice?
- Quite tricky to get all the indexes right, maybe just having guards at the top is the right thing to do

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        if(nums.size() < 2) return nums[0];
        int best = 0;
        vector<int> profit(nums.size()+2);
        profit[0] = nums[0];
        profit[1] = max(nums[1],nums[0]);
        for(int i = 2 ;i < nums.size()-1; i++){
            profit[i] = max(profit[i-1],profit[i-2]+nums[i]);
        }
        best = max(best,profit[nums.size()-2]);
        fill(profit.begin(),profit.end(),0);
        profit[1] = nums[1];
        if(nums.size() > 2) profit[2] = max(nums[2],nums[1]);
        for(int i = 3 ;i < nums.size(); i++){
            profit[i] = max(profit[i-1],profit[i-2]+nums[i]);
        }
        best = max(best,profit[nums.size()-1]);
        return best;
    }
};
```


<https://leetcode.com/problems/longest-palindromic-substring>

<https://leetcode.com/problems/palindromic-substrings>

<https://leetcode.com/problems/decode-ways>

<https://leetcode.com/problems/coin-change>

<https://leetcode.com/problems/maximum-product-subarray>

<https://leetcode.com/problems/word-break>

<https://leetcode.com/problems/longest-increasing-subsequence>

<https://leetcode.com/problems/partition-equal-subset-sum>

