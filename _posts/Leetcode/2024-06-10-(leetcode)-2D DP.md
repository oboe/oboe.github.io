<https://leetcode.com/problems/unique-paths>
Naive
- mxn grid, return number of possible unique paths that robot can take
- Terrible approach is just permuting ever single rdrd, combination
- 3Rs, 3Ds, how many permutations exist of these

```
(m+n)!
-------
m! x n!
```

```cpp
class Solution {
public:
    int uniquePaths(int m, int n) {
        long ans = 1;
        for(int i = m+n-2, j = 1; i >= max(m, n); i--, j++) 
            ans = (ans * i) / j;
        return ans;
    }
};
```

<https://leetcode.com/problems/longest-common-subsequence>
Naive
- given two strings return length of longest common subsequence
- Brute force generate all subsequences and compare, maintaining a best size
- Was on the right track, once again if it's a dp question you need to think about the recursive relation.

```cpp
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        vector<vector<int>> dp(text1.size(),vector<int>(text2.size(),0));
        for(int i = 0 ; i < text1.size();i++){
            for(int j = 0 ; j < text2.size(); j++){
                if(text1[i] == text2[j]){
                    if(i == 0 || j ==0){
                        dp[i][j] = 1;
                    } else {
                        dp[i][j] = dp[i-1][j-1] + 1;
                    }
                } else {
                    int val = 0;
                    if(i > 0 ) val = max(val,dp[i-1][j]);
                    if(j > 0 ) val = max(val,dp[i][j-1]);
                    dp[i][j] = val;
                }
            }
        }
        return dp[text1.size()-1][text2.size()-1];
    }
};
```


<https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown>
Naive
- find out max profit
- one day cooldown
- Go through every single valid buy sell 3^n
- Had the right intuition, but last action was wrong, all you need to care about is what is useful to cache. Can you buy or can you sell
- Lets go top down

```cpp
struct p_hash {
    template<class T1, class T2>
    size_t operator () (const pair<T1,T2> &p) const {
        auto h1 = hash<T1>{}(p.first);
        auto h2 = hash<T2>{}(p.second);
        return h1 ^ h2;
    }
};

class Solution {
public:
    vector<int> p = vector<int>();
    unordered_map<pair<int,bool>,int,p_hash> stateToProfit;
    int maxProfit(vector<int>& prices) {
        p = prices;
        return dfs(0,true);
    }

    int dfs(int i, bool canBuy) {
        if(i >= p.size()) return 0;
        if(stateToProfit.count(make_pair(i,canBuy)) != 0) return stateToProfit[make_pair(i,canBuy)];
        if(canBuy){
            int buy = dfs(i+1, false) - p[i];
            int nothing = dfs(i+1, true);
            stateToProfit[make_pair(i,canBuy)] = max(buy,nothing);
            return max(buy,nothing);
        } else {
            int sell = dfs(i+2, true) + p[i];
            int nothing = dfs(i+1, false);
            stateToProfit[make_pair(i,canBuy)] = max(sell,nothing);
            return max(sell,nothing);
        }
    }
};
```


<https://leetcode.com/problems/coin-change-ii>
Naive
- Return number of combinations that make up that amount
- return 0 if not found
- infinite number of each coin
- Naive is generate every single 
- change(i) = sum(change(i-x)+change(x),change(i-y)+change(y)...)
- Sharp edge with avoiding duplicate solution
- This can be avoided by only adding coins in a certain order

```cpp
class Solution {
public:
    int change(int amount, vector<int>& coins) {
        vector<vector<int>> dp(amount+1,vector<int>(coins.size()+1));
        dp[0][0] = 1;
        for(int i = 0 ; i < coins.size() ;i++){
            for(int j = 0 ; j <= amount ; j++){
                if(j-coins[i] >= 0) dp[j][i] += dp[j-coins[i]][i];
                if(i != 0) dp[j][i] += dp[j][i-1];
            }
        }
        return dp[amount][coins.size()-1];
    }
};
```


<https://leetcode.com/problems/target-sum>
Naive
- Build expression, return number of different expressions that you can build
- that hits the target!
- Each num can be +ve or -ve
- so recursive relation is likely
- t(amount,numsPos) = sum(t(a+x,numsPos-1),t(a-x,numsPos-1))
- Lets go top down this time


```cpp
class Solution {
public:
    vector<int> n;
    int findTargetSumWays(vector<int>& nums, int target) {
        n = nums;
        unordered_map<int,vector<int>> dp;
        int remaining = accumulate(nums.begin(),nums.end(),0);
        return dfs(target, nums.size()-1, remaining,dp);
    }

    int dfs(int amount, int numsIndex, int remaining, unordered_map<int,vector<int>>& dp){
        if(numsIndex < 0 && amount == 0) return 1;
        if(numsIndex < 0) return 0;
        if(remaining < abs(amount)) return 0;
        if(dp.count(amount) != 0 && dp[amount].size() > numsIndex && dp[amount][numsIndex] != 0) return dp[amount][numsIndex];
        int l = dfs(amount+n[numsIndex],numsIndex-1, remaining-n[numsIndex] ,dp);
        int r = dfs(amount-n[numsIndex],numsIndex-1, remaining-n[numsIndex],dp);
        if(dp.count(amount) == 0) dp[amount] = vector<int>(n.size());
        dp[amount][numsIndex] = l + r;
        return dp[amount][numsIndex];
    }
};
```

<https://leetcode.com/problems/interleaving-string>
Naive
- return bool, on if a string is the interleaved combination of two other strings
- naive solution can just be permuting every single permutation and checking i it matches the target
- Or maintain pointer to heads of both input strings, greedily taking the valid character, and if both header characters are valid then perform search on both of those subtrees
- Naively doing this is a 2^n complexity solution which isn't really an option, how can I avoid computing on duplicate subtrees?

Good
- Create a 2d array to hold the
- num(a-pos, b-pos)  = max(num(a-pos-1,b-pos) + 1 (if matching a),num(a-pos, b-pos-1) + 1(if matching b)

```cpp
class Solution {
public:
    bool isInterleave(string s1, string s2, string s3) {
        if(s1.size() + s2.size() != s3.size()) return false;
        vector<vector<int>> dp(s1.size()+1,vector<int>(s2.size()+1));
        for(int i = 0 ; i< s1.size() ;i++){
            dp[i+1][0] = dp[i][0];
            if(s1[i] == s3[dp[i][0]]) dp[i+1][0]++;
        }
        for(int j = 0 ;j < s2.size() ; j++){
            dp[0][j+1] = dp[0][j];
            if(s2[j] == s3[dp[0][j]]) dp[0][j+1]++;
        }
        for(int i = 1 ;i <= s1.size();i++){
            for(int j = 1 ; j <= s2.size() ; j++){
                if(s1[i-1] == s3[dp[i-1][j]]) dp[i][j] = max(dp[i][j], dp[i-1][j] + 1);
                if(s2[j-1] == s3[dp[i][j-1]]) dp[i][j] = max(dp[i][j], dp[i][j-1] + 1);
            }
        }
        return (dp[s1.size()][s2.size()] >= s3.size());
    }
};
```

<https://leetcode.com/problems/longest-increasing-path-in-a-matrix>
Naive
- Return the length of increasing path
- terrible solution is just get every path and check if its increasing and maintain a best
- Better solution is to do a search starting at each index, i'll go with dfs, and to just search all directions, maintaining a list of visited, treading down the tree until valid. AKA just a full search
- And I can notice that if I start at position 6, I can almost reuse the solution, I need to somehow consider visited nodes
- Actually I don't need to care about visited nodes because of the longest increasing path restriction I cannot actually use those positions
- The order is important! When is it right to return a cached value, only when it's valid, if its non increasing then you shouldnt return the cached value!


```cpp
class Solution {
public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        vector<vector<int>> lip(matrix.size(),vector<int>(matrix[0].size()));
        int ans = 0;
        for(int i = 0 ; i < matrix.size() ;i++){
            for(int j = 0 ; j < matrix[0].size();j++){
                ans = max(ans,dfs(i,j,-1,lip,matrix));
            }
        }
        return ans;
    }

    int dfs(int x, int y, int last, vector<vector<int>>& lip, vector<vector<int>>& matrix){
        if(x < 0 || x >= matrix.size()) return 0;
        if(y < 0 || y >= matrix[0].size()) return 0;
        int curr = matrix[x][y];
        if(curr <= last) return 0;// non increasing
        if(lip[x][y] != 0) return lip[x][y];
        // adjacents
        int l = dfs(x-1,y,curr,lip,matrix);
        int r = dfs(x+1,y,curr,lip,matrix);
        int u = dfs(x,y-1,curr,lip,matrix);
        int d = dfs(x,y+1,curr,lip,matrix);
        //cache and return
        lip[x][y] = max(max(l,r),max(u,d)) + 1;
        return lip[x][y];
    }
};
```

<https://leetcode.com/problems/distinct-subsequences>
Naive
- get number of subsequences that equal t
- had to use a unsigned long long to store intermediate values
```
f(si,ti) = f(si-1,ti)
if(s[si] == t[ti]) += f(si-1,ti-1)
```

```cpp
class Solution {
public:
    int numDistinct(string s, string t) {
        vector<vector<long long unsigned>> dp(s.size()+1, vector<long long unsigned>(t.size()+1));
        for(int i = 0 ; i <= s.size() ;i++){
            dp[i][0] = 1;
        }
        for(int i = 1 ; i <= s.size() ;i++){
            for(int j = 1 ; j <= t.size() ;j++){
                dp[i][j] += dp[i-1][j];
                if(s[i-1] == t[j-1]) dp[i][j] += dp[i-1][j-1];
            }
        }
        return dp[s.size()][t.size()];
    }
};
```

<https://leetcode.com/problems/edit-distance>
Naive
- Think clearly about the recursive relation.
- How can I calculate f() for prefix 0..a and 0..b?
- It's the prefix, not the direct character which matters!

```
minDistance(idx1,idx2) = min(curr, )
```

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        vector<vector<int>> dp(word1.size()+1,vector<int>(word2.size()+1,INT_MAX));
        for(int i = 0 ; i< dp.size();i++){
            dp[i][0] = i;
        }
        for(int i = 0 ;i< dp[0].size();i++){
            dp[0][i] = i;
        }
        dp[0][0] = 0;
        for(int i = 1; i < dp.size();i++){
            for(int j = 1 ; j < dp[0].size();j++){
                dp[i][j] = min(dp[i][j],dp[i][j-1]+1);
                dp[i][j] = min(dp[i][j],dp[i-1][j]+1);
                if(word1[i-1] == word2[j-1]){
                    dp[i][j] = min(dp[i][j],dp[i-1][j-1]);
                } else {
                    dp[i][j] = min(dp[i][j],dp[i-1][j-1] + 1);
                }
            }
        }
        int ans = dp[word1.size()][word2.size()];
        if(ans == INT_MAX) ans = 0;
        return ans;
    }
};
```

<https://leetcode.com/problems/burst-balloons>
Naive
- pop all balloons, popping balloon gets you higher coins if adjacent balloons have the largest numbers
- naive solution is to do a brute force search, pop every single balloon in every order.
- This is actually all permutations and therefore n!
- So naive optionality tree has nums branches and, each subsequent tree has n-1 balloons.
- Also greedy intuition that you want to pop the largest balloons last
- Issue with this option tree is that deduplicating subtrees is difficult because we need to care about balloons you've popped previously, you can't pop them again, and those values change what balloons are adjacent
- there is a clear subproblem deduping we can do as the answer for any balloon array it's the same answer in the end
- Let's try a top down

```cpp
// TIME LIMIT EXCEEDED

class Solution {
public:
    int maxCoins(vector<int>& nums) {
        unordered_map<string,int> strToMaxCoins;
        return dfs(nums,strToMaxCoins);
    }

    int dfs(vector<int>& nums,unordered_map<string,int>& strToMaxCoins){
        if(nums.size() <= 0) return 0;
        string converted = convert(nums);
        if(strToMaxCoins.count(converted) != 0) return strToMaxCoins[converted];
        int best = 0;
        for(int i = 0 ;i  < nums.size() ;i++){
            int curr = nums[i];
            int profit = nums[i];
            if(i > 0) profit *= nums[i-1];
            if(i < nums.size()-1) profit *= nums[i+1];
            nums.erase(next(nums.begin(),i));
            best=max(best,dfs(nums,strToMaxCoins)+profit);
            nums.insert(nums.begin()+i,curr);
        }
        strToMaxCoins[converted] = best;
        return best;
    }

    string convert(vector<int>& balloons){
        string ans = "";
        for(int i : balloons){
            ans += to_string(i) + ",";
        }
        return ans;
    }
};
```

Good
- Doing above is not an option as the subarrays I'm caching are still 2^n
- It is every single subsequence, i'm going through all subsequences
- Instead do it in reverse, this lets us cache the L and Rs instead, how snazzy!

<https://leetcode.com/problems/regular-expression-matching>
Naive
- Always start these kinds of questions recursively
