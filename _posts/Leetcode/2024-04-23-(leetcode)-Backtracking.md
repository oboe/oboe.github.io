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

https://leetcode.com/problems/permutations/

https://leetcode.com/problems/subsets-ii/

https://leetcode.com/problems/combination-sum-ii/

https://leetcode.com/problems/word-search/

https://leetcode.com/problems/palindrome-partitioning/

https://leetcode.com/problems/letter-combinations-of-a-phone-number/

https://leetcode.com/problems/n-queens/

