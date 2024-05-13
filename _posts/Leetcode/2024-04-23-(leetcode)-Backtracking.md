## Context
Some questions require a complete search. When these brute force solutions are too complicated, you'll need to use better strategies.

Theres two common things you'll need to search subsets and permutations.
#### Subsets
Subsets are all the possibilities of a set. AB, A, B and empty set.

One way you can do this is recursively.
```cpp
vector<int> subset;
void search(int k) {
	if (k == n) {
	   // process subset
	} else {
	   search(k+1);
	   subset.push_back(k);
	   search(k+1);
	   subset.pop_back();
	} 
}
```

Another way is iteratively.
```cpp
for (int b = 0; b < (1<<n); b++) {
	vector<int> subset;
	for (int i = 0; i < n; i++) {
	   if (b&(1<<i)) subset.push_back(i);
	}
}
```
#### Permutations
Permutations are all possible orderings. AB and BA.

You can do it recursively.
```cpp
 void search() {
	if (permutation.size() == n) {
	   // process permutation
	} else {
	   for (int i = 0; i < n; i++) {
		   if (chosen[i]) continue;
		   chosen[i] = true;
		   permutation.push_back(i);
		   search();
		   chosen[i] = false;
		   permutation.pop_back();
	   }
} }
```

Or iteratively, using the next_permutation function!
```cpp
vector<int> permutation;
for (int i = 0; i < n; i++) {
	permutation.push_back(i);
}
sort(permutation.begin(),permutation.end());
do {
	// process permutation
} while (next_permutation(permutation.begin(),permutation.end()));
```
## Qs

https://leetcode.com/problems/subsets/
Naive
- generate all subsets
- Just go through and double ans with possible vectors

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> ans;
        ans.push_back({});
        for(int i : nums){
            vector<vector<int>> additions;
            for(vector<int> v : ans){
                vector<int> c = v;
                c.push_back(i);
                additions.push_back(c);
            }
            ans.insert(end(ans),additions.begin(),additions.end());
        }
        return ans;
    }
};
```

Good
- You can do iterate with int dealing with 2s to get all subsets, which would be marginally faster

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> ans;
        for(int i = 0 ; i < pow(2,nums.size()) ; i++){
            vector<int> curr;
            for(int j = 0 ; j < nums.size() ; j++){
                if(i & (1<<j)){
                    curr.push_back(nums[j]);
                }
            }
            ans.push_back(curr);
        }
        return ans;
    }
};
```

https://leetcode.com/problems/combination-sum/
Naive
- iterate through all candidate subsets, checking if they match the target
- Read the goddamn question, numbers can be selected an unlimited number of times!


```cpp
class Solution {
public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<int> subset;
        set<vector<int>> ans;
        search(candidates.size(),target,subset, ans, candidates);
        vector<vector<int>> aa;
        for(auto ll: ans){
            aa.push_back(ll);
        }
        return aa;
    }

    void search(int max,int target, 
    vector<int>& subset,set<vector<int>>& ans,
    vector<int>& candidates){
        int val = accumulate(subset.begin(),subset.end(),0);
        if(val == target){
            vector<int> newSubset = subset;
            sort(newSubset.begin(),newSubset.end());
            ans.insert(newSubset);
        } else {
            if(val > target) return;
            for(int i = 0 ; i < max ;i++){
                subset.push_back(candidates[i]);
                search(max,target,subset,ans,candidates);
                subset.pop_back();
            }
        }
    }
};
```

https://leetcode.com/problems/permutations/
Naive
- return all permutations
- no frills

```cpp
class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        vector<int> permutation;
        vector<bool> chosen(nums.size(),false);
        vector<vector<int>> ans;
        search(permutation,chosen,nums,ans);
        return ans;
    }

    void search(vector<int>& permutation,vector<bool> chosen,
    vector<int>& nums,vector<vector<int>>& ans){
        if(permutation.size() == nums.size()){
            ans.push_back(permutation);
        } else {
            for(int i = 0 ; i < nums.size();i++){
                if(chosen[i]) continue;
                chosen[i] = true;
                permutation.push_back(nums[i]);
                search(permutation,chosen,nums,ans);
                chosen[i] = false;
                permutation.pop_back();
            }
        }
    }
};
```

https://leetcode.com/problems/subsets-ii/
Naive
- Below
- You can actually sort the nums, and skip through the depth, if we've done a search already on depth.

```cpp
class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        set<vector<int>> ans;
        vector<int> subset;
        search(0,subset,ans,nums);
        vector<vector<int>> vecans;
        for(auto a: ans){
            vecans.push_back(a);
        }
        return vecans;
    }

    void search(int depth,vector<int>& subset, set<vector<int>>& ans, vector<int>& nums){
        if(depth == nums.size()){
            vector<int> s = subset;
            sort(s.begin(),s.end());
            ans.insert(s);
        } else {
            //search path where current element is not in set.
            search(depth+1,subset,ans,nums);
            //search path where current element is in set
            subset.push_back(nums[depth]);
            search(depth+1,subset,ans,nums);
            subset.pop_back();
        }
    }
};
```

https://leetcode.com/problems/combination-sum-ii/
Naive
- find all unique combinations where candidate sum to target
- Each number can only be used once
- Return the number of candidates and **cannot contain duplicate combinations**
- Recursively iterate through all subsets, pruning when we're over target.

```cpp
//not really clean
class Solution {
public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        vector<int> subset;
        vector<vector<int>> ans;
        sort(candidates.begin(),candidates.end());
        search(0,subset,target,candidates,ans);
        return ans;
    }

    void search(int depth,vector<int>& subset, int target, vector<int>& candidates,vector<vector<int>>& ans ){
        int val = accumulate(subset.begin(),subset.end(),0);
        if(val == target){
            vector<int> cp = subset;
            ans.push_back(cp);
        } else {
            if (val > target) return;
            if(depth>=candidates.size()) return;
            subset.push_back(candidates[depth]);
            search(depth+1,subset,target,candidates,ans);
            subset.pop_back();
            int i = 1;
            bool found = false;
            for(i = 1; i < candidates.size()-depth;i++){
                if(depth+i>=candidates.size()) break;
                if(candidates[depth] != candidates[depth+i]){
                    found = true;
                    break;
                }
            }
            if (found) search(depth+i,subset,target,candidates,ans);
        }
    }
};
```

https://leetcode.com/problems/word-search/

https://leetcode.com/problems/palindrome-partitioning/

https://leetcode.com/problems/letter-combinations-of-a-phone-number/

https://leetcode.com/problems/n-queens/

