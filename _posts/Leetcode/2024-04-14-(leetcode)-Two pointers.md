https://leetcode.com/problems/valid-palindrome/
Good:
- Just a simple left right pointer: n, 1 space

```cpp
class Solution {
public:
    bool isPalindrome(string s) {
        int l = 0;
        int r = s.size();
        while(l <= r){
            char charL = s[l];
            char charR = s[r];
            if (!isalnum(charL)){
                l++;
                continue;
            }
            if (!isalnum(charR)){
                r--;
                continue;
            }
            charL = tolower(charL);
            charR = tolower(charR);
            if (charL != charR) {
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
```

https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
Good:
- Same as above: n, 1 space

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int l = 0;
        int r = numbers.size()-1;
        while(l < r){
            if (numbers[l] + numbers[r] == target) {
                return {l+1,r+1};
            }
            if (numbers[l] + numbers[r] < target) {
                l++;
            }
            else {
                r--;
            }
        }
        return {l+1,r+1};
    }
};
```
https://leetcode.com/problems/3sum/
Naive:
- 3 for loops: n^3, 1 space

Good
- sort (val,index) pairs, 1 fixed val, 2 pointers: n^2, n space
- better would be creating a hashing function for the unordered_map
- or just skipping the duplicates inline somehow


```cpp
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<pair<int,int>> valIdx;
        for(int i = 0 ; i < nums.size(); i++){
            valIdx.push_back(make_pair(nums[i],i));
        }
        sort(valIdx.begin(), valIdx.end());
        vector<vector<int>> ans;
        set<vector<int>> ans2;
        for(int i = 0 ; i < valIdx.size()-2; i++){
            int val1 = valIdx[i].first;
            int idx1 = valIdx[i].second;
            int l = i+1;
            int r = valIdx.size()-1;
            while(l<r){
                int val2 = valIdx[l].first;
                int idx2 = valIdx[l].second;
                int val3 = valIdx[r].first;
                int idx3 = valIdx[r].second;
                if(val1 + val2 + val3 == 0){
                    ans2.insert({val1,val2,val3});
                }
                if(val1 + val2 + val3 > 0){
                    r--;
                }
                else {
                    l++;
                }
            }
        }
        for(auto a : ans2){
            ans.push_back(a);
        }
        return ans;
    }
};
```

https://leetcode.com/problems/container-with-most-water/description/

https://leetcode.com/problems/trapping-rain-water/description/

