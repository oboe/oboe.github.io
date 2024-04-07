
https://leetcode.com/problems/contains-duplicate/

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

https://leetcode.com/problems/valid-anagram/description/

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


https://leetcode.com/problems/two-sum/description/

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
https://leetcode.com/problems/group-anagrams/description/

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

https://leetcode.com/problems/top-k-frequent-elements/description/

https://leetcode.com/problems/product-of-array-except-self/description/

https://leetcode.com/problems/valid-sudoku/description/