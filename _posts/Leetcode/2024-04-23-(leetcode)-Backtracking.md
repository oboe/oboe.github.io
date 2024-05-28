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

#### Backtracking
What does it mean to backtrack? It's to incrementally build candidates to the solutions and abandons a candidate as soon as it determines that the candidate cannot lead to a final solution.
## Qs

<https://leetcode.com/problems/subsets>
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

<https://leetcode.com/problems/combination-sum>
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

<https://leetcode.com/problems/permutations>
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

<https://leetcode.com/problems/subsets-ii>
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

<https://leetcode.com/problems/combination-sum-ii>
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

<https://leetcode.com/problems/word-search>
Naive
 - find out if a grid contains a single word
 - Same letter may not be used more than once

Good
- Go through all indexes, starting a search
- Each search will have a k, a copy of the grid to keep track of visited and do a search
- The search can just return a bool, as that's what we're looking for

```cpp
class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        if(word.size()==0) return true;
        if(board.size()==0) return false;

        vector<vector<bool>> visited(board.size(),vector<bool>(board[0].size(),false));
        for(int i = 0 ; i < board.size();i++){
            for(int j = 0 ;  j < board[0].size() ;j++){
                bool ans = search(i,j,0,visited,board,word);
                if(ans) return true;
            }
        }
        return false;
    }

    bool search(int x, int y,int pos, vector<vector<bool>>& visited,vector<vector<char>>& board, string word){
        // is x y valid?
        if(x<0 || x >=board.size()) return false;
        if(y<0 || y >=board[0].size()) return false;

        // is x y char match the word?
        // and if its the last one, return true
        if(visited[x][y]) return false;
        char curr = board[x][y];
        //cout << "curr: " << curr << "\n";
        if(word[pos] != curr) return false;
        if(pos >= word.size() -1) return true;

        // if its not the last one then do searches on adjacents
        visited[x][y] = true;
        bool ans = search(x+1,y,pos+1,visited,board,word) 
        || search(x-1,y,pos+1,visited,board,word)
        || search(x,y+1,pos+1,visited,board,word) 
        || search(x,y-1,pos+1,visited,board,word);
        visited[x][y] = false;
        return ans;
    }
};
```

<https://leetcode.com/problems/palindrome-partitioning>
Naive
- Return every single palindrome partitioning
- Cant really think of a clean brute force method here
- Always try think of a brute force method, you just needed to iterate through it, adding and popping valid substrings

```cpp
class Solution {
public:
    vector<vector<string>> ans;
    vector<vector<string>> partition(string s) {
        vector<string> input;
        search(input, 0,s);
        return ans;
    }

    void search(vector<string>& curr, int pos, string s){
        if(pos >= s.size()) ans.push_back(curr);
        string pal = "";
        for(int i = pos ;i < s.size() ;i++){
            pal += s[i];
            if(isPalindrome(pal)){
                curr.push_back(pal);
                search(curr, i+1, s);
                curr.pop_back();
            }
        }
    }

    bool isPalindrome(string pal){
        for(int i = 0 ;i < pal.size()/2 ; i++){
            char l = pal[i];
            char r = pal[pal.size()-1-i];
            if(l!=r) return false;
        }
        return true;
    }
};
```

<https://leetcode.com/problems/letter-combinations-of-a-phone-number>
Naive
- return all possible letter combinations that the number could represent
- 222 = aaa, ab, ba, c
- Read the question wrong and implemented solution that works for the standard double press letter phone style, so I don't care as I feel what i've done is the cool solution

```cpp
class Solution {
public:
    vector<string> ans;
    unordered_map<char, vector<char>> mapping{
        {'2', vector<char>{'a','b','c'}},
        {'3', vector<char>{'d','2','f'}},
        {'4', vector<char>{'g','h','i'}},
        {'5', vector<char>{'j','k','l'}},
        {'6', vector<char>{'m','n','o'}},
        {'7', vector<char>{'p','q','r','s'}},
        {'8', vector<char>{'t','u','v'}},
        {'9', vector<char>{'w','x','y','z'}},
    };
    vector<string> letterCombinations(string digits) {
        string curr; 
        search(0,digits,curr);
        return ans;
    }

    void search(int pos, string digits, string& curr){
        if(pos >= digits.size()) ans.push_back(curr);
        char same = digits[pos];
        for(int i = pos ; i < digits.size();i++){
            if(digits[i] != same) break;
            curr += mapping[same][i-pos];
            search(i+1,digits,curr);
            curr.pop_back();
        }
    }
};
```

<https://leetcode.com/problems/n-queens>
Naive
- Generate every single n queen permutation and check if it's valid

Good
- Iteratively place n queens on each row, until you hit the end
- n^4

```cpp
class Solution {
public:
    vector<vector<string>> ans;
    vector<vector<string>> solveNQueens(int n) {
        vector<string> curr;
        search(curr,0,n);
        return ans;    
    }

    void search(vector<string>& curr, int row, int n){
        //complete?
        if(row >= n) {
            ans.push_back(curr);
            return;
        }
        // iterate through all possible qs
        for(int i = 0 ; i < n; i++){
            string newRow(n,'.');
            newRow[i] = 'Q';
            curr.push_back(newRow);
            if(isValid(curr,n)){
                search(curr,row+1,n);
            }
            curr.pop_back();
        }
    }

    bool isValid(vector<string> curr,int n){
        if(curr.size() ==0) return true;
        vector<pair<int,int>> coods;
        //col
        vector<bool> colValid(n,false);
        for(int i = 0 ; i < curr.size(); i++){
            for(int j = 0 ; j < curr[0].size() ;j++){
                if(curr[i][j] == '.') continue;
                coods.push_back({i,j});
                if(colValid[j]) {
                    return false;
                }
                colValid[j] = true;
            }
        }
        // diagonal
        for(int i = 0 ; i < coods.size(); i++){
            for(int j = i+1 ; j < coods.size() ;j++){
                int xDiff = abs(coods[i].first - coods[j].first);
                int yDiff = abs(coods[i].second - coods[j].second);
                if(xDiff == yDiff) {
                    return false;
                }
            }
        }
        return true;
    }
};
```