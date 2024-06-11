## Context
Use it when you want to
1. Find an optimal solution
2. Count the number of solutions

To solve DP, find the recursive function, what sub problems can you solve to calculate the answer to your problem?

The key of DP is to use memoization to cache the sub problem values efficiently.

This is why theres two ways of doing DP problems, top down or bottom up (usually called tabulation, avoid stack calls). Are you going down or up the recursive tree?


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
Naive
- return the longest palindromic substring
- Naive is just nested for loop
- Can also just do it naively and memoize

```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        string best = "";
        for(int i = 0 ;i < s.size();i++){
            //odd
            int oddCount = 0;
            for(int j = 1 ; j <= s.size() ;j++){
                if(i+j >= s.size() || i-j < 0) break;
                if(s[i-j] == s[i+j]){
                    oddCount = j;
                } else{
                    break;
                }
            }
            if(best.size() < (oddCount*2)+1) best = s.substr(i-oddCount,(oddCount*2)+1);
            //even
            int evenCount = 0;
            for(int j = 1 ; j <= s.size() ;j++){
                if(i+j >= s.size() || i-j+1 < 0) break;
                if(s[i-j+1] == s[i+j]){
                    evenCount = j;
                }else{
                    break;
                }
            }
            if(best.size() < evenCount*2) best = s.substr(i-evenCount+1,evenCount*2);

        }
        return best;
    }
};
```

<https://leetcode.com/problems/palindromic-substrings>
Naive
- return the number of substrings in it

```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int ans = 0;
        for(int i = 0 ;i < s.size();i++){
            //odd
            ans += 1;
            for(int j = 1 ; j <= s.size() ;j++){
                if(i+j >= s.size() || i-j < 0) break;
                if(s[i-j] == s[i+j]){
                    ans+=1;
                } else{
                    break;
                }
            }
            //even
            for(int j = 1 ; j <= s.size() ;j++){
                if(i+j >= s.size() || i-j+1 < 0) break;
                if(s[i-j+1] == s[i+j]){
                    ans+=1;
                }else{
                    break;
                }
            }

        }
        return ans;
    }
};
```
<https://leetcode.com/problems/decode-ways>
Naive
- return number of ways to decode a string
- decode(i) = (decode(i-1)+1) + (decode(i-2)+1)
- where the i-2 one is only valid when the 2 chars are under 26

```cpp
class Solution {
public:
    int numDecodings(string s) {
        vector<int> v(s.size()+2,0);
        v[0] = 1;
        for(int i = 0 ;i < s.size();i++){
            if(s[i] != '0'){
                v[i+1] += v[i];
            }
            if(i+1 < s.size() && isValid(s[i],s[i+1])){
                v[i+2] += v[i];
            }
        }
        return v[s.size()];
    }

    bool isValid(char a, char b){
        if(a != '1' && a != '2') return false;
        string s = "";
        s.push_back(a);
        s.push_back(b);
        int i = stoi(s);
        return (i <= 26);
    }
};
```
<https://leetcode.com/problems/coin-change>
Naive
- given list of coins, and goal
- get fewest number of coins that you need to make up that amount
- unique coins, can use as many times as you want
- So we could just brute force every single coin combination

Good
- need to return the number of coins to reach pos
- num(i) = min(num(i-x) + 1 .... num(i-y) + 1)
- few ways to do this bottom up and top down

```cpp
// Bottom up
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> v(amount+1,INT_MAX);
        v[0] = 0;
        for(int i = 0 ; i < amount ;i++){
            for(int coin : coins){
                if((long)i+(long)coin > (long)amount) continue;
                if(v[i] == INT_MAX) continue;
                v[i+coin] = min(v[i+coin],v[i]+1);
            }
        }
        if(v[amount] == INT_MAX) return -1;
        return v[amount];
    }
};
```

```cpp
// top down
class Solution {
public:
    vector<int> v = vector<int>(100000,INT_MAX);
    int coinChange(vector<int>& coins, int amount) {
        if(amount == 0) return 0;
        if(amount < 0) return -1;
        if(v[amount] != INT_MAX) return v[amount];
        int least = INT_MAX;
        for(int coin : coins){
            if(amount-coin < 0) continue;
            int val = coinChange(coins, amount-coin);
            if(val != -1) least = min(least, val);
        }
        if(least == INT_MAX){
            v[amount] = -1;
            return -1;
        }
        else {
            v[amount] = least + 1;
            return least + 1;
        }
    }
};
```

<https://leetcode.com/problems/maximum-product-subarray>
Naive
- just i, j nested loop and brute force it
- max ending at:
- maxEndingAt(i) = max(maxEndingAt(i-1) * current(i) ,current(i))
- caveat is maxEndingAt(i) needs to be max neg or pos so need to maintain both
- lets go bottom up

```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int maxSum = 0;
        int minSum = 0;
        int ans = INT_MIN;
        for(int i = 0; i < nums.size();i++){
            if(i == 0){
                maxSum = nums[i];
                minSum = nums[i];
                ans = max(ans, maxSum);
                continue;
            }
            if(nums[i] > 0){
                maxSum = max(nums[i], maxSum*nums[i]);
                minSum = minSum*nums[i];
            } else { // -ve
                maxSum = min(nums[i], maxSum*nums[i]);
                minSum = minSum*nums[i];
                swap(maxSum,minSum);
            }
            ans = max(ans, maxSum);
        }
        return ans;
    }
};
```


<https://leetcode.com/problems/word-break>
Naive
- Return true or false if it's possible for the word to be segmentated
- combine every single word, until you get the target word
- Feels like fairly trivially 
- break(word) = break(word-k) && break(k)
- let's go top down

```cpp
class Solution {
public:
    unordered_map<string,bool> breaks;
    bool wordBreak(string s, vector<string>& wordDict) {
        if(s.size() ==0) return true;
        if(breaks.count(s)) return breaks[s];
        for(string word: wordDict){
            if(match(s,word)){
                string remainingStr = s.substr(word.size());
                bool val = wordBreak(remainingStr,wordDict);
                breaks[remainingStr] = val;
                if(val) return true;
            }
        }
        breaks[s] = false;
        return false;
    }

    bool match(string a, string b){
        if(b.size() > a.size()) return false;
        for(int i = 0 ; i < b.size() ;i++){
            if(a[i] != b[i]) return false;
        }
        return true;
    }
};
```


<https://leetcode.com/problems/longest-increasing-subsequence>
Naive
- return the longest strictly increasing subsequence, doesn't need to be connected
- Try every subset, checking if its strictly increasing and maintaining a best.
- A think there might be a recursive relation here.
- I feel that LIS(i) = max((if larger than last)LIS(i-1) + 1, 1)
- wait this doens't work, do i need to also maintain LIS(i) where it doens't contain that value?
- Could just do a n^2 where inner loops through all previous LIS 
- Take note of the N which is 1e3, so an n^2 is possible

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> v(nums.size()+1,1);
        int best = 1;
        for(int i = 0 ;i < nums.size() ;i++){
            for(int j = 0 ; j < i ;j++){
                if(nums[j] >= nums[i]) continue;
                v[i] = max(v[i], v[j]+1);
                best = max(best, v[i]);
            }
        }
        return best;
    }
};
```

<https://leetcode.com/problems/partition-equal-subset-sum>
Naive
- Find out if I can split array into two subsets that they can sum together
- Brute force is try every single subset
- positive numbers only, so this means i could pass and find out the total sum, to find out what subset I need to insert to get the required total
- The key question is how can can I avoid doing duplicate work here?
- I guess this is 2d dp :I

```cpp
class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int target = accumulate(nums.begin(),nums.end(),0);
        if(target%2 !=0) return false;
        target = target/2;
        unordered_set<int> s;
        s.insert(0);
        for(int num : nums){
            vector<int> newAddtions;
            for(int i : s){
                if(i+num > target) continue;
                if(i+num == target) return true;
                newAddtions.push_back(i+num);
            }
            s.insert(newAddtions.begin(),newAddtions.end());
        }
        return false;
    }
};
```