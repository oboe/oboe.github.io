Hashing is great to check for duplicates and to group things.


<<https://leetcode.com/problems/contains-duplicate>>

Naive
- Sort and pass: nlogn time, 1 space

Good
- Hashset and pass: n time, n space

```cpp
class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> set;
        for (int i = 0 ;i < nums.size() ; i++) {
            if (set.count(nums[i]) != 0) {
                return true;
            }
            set.insert(nums[i]);
        }
        return false;
    }
};

```

<<https://leetcode.com/problems/valid-anagram/description>>

Naive
- Sort and pass: nlogn, 1 space

Good
- Hashmap to get charCounts: n, nspace

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        unordered_map<char,int> charMap;
        if (s.size() != t.size()){
            return false;
        }
        for(int i = 0 ;i < s.size() ; i++){
            charMap[s[i]]++;
        }
        for(int i = 0 ;i < t.size() ; i++) {
            int val = charMap[t[i]];
            if (val == 0) {
                return false;
            }
            charMap[t[i]]--;
        }
        return true;
    }
};
```


<<https://leetcode.com/problems/two-sum/description>>

Naive
- nested loop: n^2, 1 space
-  encode index, sort, two pointer: nlogn, 1 space

Good
- hashmap: n,nspace

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> mp;
        for (int i = 0; i < nums.size(); ++i) {
            if (mp.count(target - nums[i])) return {i, mp[target - nums[i]]};
            mp[nums[i]] = i;
        }
        return {};
    }
};
```
<<https://leetcode.com/problems/group-anagrams/description>>

Naive
- pop one, find all matching anagrams, do this again
- create a sorted version of each string, sort the entire strings, pop each matching string with two pointers

Good
- Instead of using a hashmap just bit encode it 2^26, or just a 26 length array
- **Create a key that represents the anagram (charmap/sort) and pass: n, n space**
- When you want to group elements of a vector ask yourself if theres a way to encode a key so you can use a hashmap to do it in a single pass


```cpp
class Solution {
public:
    string getCharMap(string s) {
        vector<int> cMap(26,0);
        for (int i = 0 ; i < s.size() ; i++) {
            int c = s[i];
            cMap[(c - 'a')]++;
        }
        string ans = "";
        for (int i = 0 ; i < cMap.size() ;i++) {
            ans += cMap[i];
        }
        return ans;
    }

    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        vector<vector<string>> ans;
        unordered_map<string,vector<string>> stringToMap;
        for(int i = 0 ; i < strs.size() ; i++){
            stringToMap[getCharMap(strs[i])].push_back(strs[i]);
        }
        for(auto kv : stringToMap) {
            ans.push_back(kv.second);
        }
        return ans;
    }
};
```

<<https://leetcode.com/problems/top-k-frequent-elements/description>>
Naive
- Sort, pass through with map, sort map results: nlogn, n space

Good
- Use a priority queue: nlogk, nspace

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end());
        unordered_map<int,int> numToFreq;
        for(int i = 0 ; i < nums.size() ; i++) {
            numToFreq[nums[i]]++;
        }
        vector<pair<int,int>> freqNumPairs;
        for(auto kv : numToFreq){
            freqNumPairs.push_back(make_pair(kv.second,kv.first));
        }
        sort(freqNumPairs.rbegin(),freqNumPairs.rend());
        vector<int> ans;
        for(int i = 0 ; i < k ; i++){
            ans.push_back(freqNumPairs[i].second);
        }
        return ans;
    }
};
```

<<https://leetcode.com/problems/product-of-array-except-self/description>>

Just maths?

```cpp
class Solution {
    // [b*c,a*c,a*b]
    // [1,a,ab]
    // [bc,b,1]
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        vector<int> ans(nums.size(), 1);
        int last = 1;
        for(int i = 0 ; i < nums.size() ; i++){
            ans[i] = ans[i]*last;
            last = last * nums[i];
        }
        last = 1;
        for(int i = nums.size() -1 ; i >= 0 ; i-- ){
            ans[i] = ans[i]*last;
            last = last * nums[i];
        }
        return ans;
    }
};
```

<<https://leetcode.com/problems/valid-sudoku/description>>
Straightforward

```cpp
class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        for(vector<char> row : board){
            if (!isValidRow(row)) {
                return false;
            }
        }
        for(int i = 0 ; i < 9 ; i++){
            if (!isValidCol(i,board)) {
                return false;
            }
        }
        for(int i = 0 ; i < 3 ; i++){
            for(int j = 0 ; j < 3 ;j++){
                if (!isValidBox(i,j,board)) {
                   return false;
                }
            }
        }
        return true;
    }

    bool isValidRow(vector<char> row) {
        unordered_set<char> cMap;
        for(char c : row) {
            if (c != '.' && cMap.count(c) != 0) {
                return false;
            }
            cMap.insert(c);
        }
        return true;
    }

    bool isValidCol(int colNum, vector<vector<char>>& board) {
        unordered_set<char> cMap;
        for(int i = 0 ; i < 9 ; i++) {
            char c = board[i][colNum];
            if (c != '.' && cMap.count(c) != 0) {
                return false;
            }
            cMap.insert(c);
        }
        return true;
    }

    bool isValidBox(int boxX, int boxY, vector<vector<char>>& board) {
        unordered_set<char> cMap;
        for(int i = 0 ; i < 9 ; i++){
            if ((boxX*3) > i) {
                continue;
            }
            if ((boxX + 1)*3 <= i ){
                continue;
            }
            for(int j = 0 ; j < 9 ; j++){
                if ((boxY*3) > j) {
                    continue;
                }
                if ((boxY + 1)*3 <= j ){
                    continue;
                }
                char c = board[i][j];
                if (c != '.' && cMap.count(c) != 0) {
                    return false;
                }
                cMap.insert(c);
            }
        }
        return true;
    }
};
```

<<https://leetcode.com/problems/longest-consecutive-sequence>>
Naive
- hashmap