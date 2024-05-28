There are three main ways to think about doing binary searches.

#### (1) Inclusive bounds
- Keep the target within the l, r bounds
- Break when l and r are next to each other

```cpp
while (l + 1 < r) {
	Integer m = l + (r - l) / 2; // prefer std::midpoint in C++20
	if (isFalse(m)) {
		l = m;
	} else {
		r = m;
	}
}
return r;
```
#### (2) Non inclusive bounds
- Skip target within l, r bounds
- You should update ans at each iteration as you will shrink your bounds without the ans

```cpp
while (l <= r) {
	Integer m = l + (r - l) / 2; // prefer std::midpoint in C++20
	if (isFalse(m)) {
		l = m + 1;
	} else {
		ans = m;
		r = m - 1;
	}
}
return ans;
```
#### (3) Partial bounds
- Haven't thought too deeply about this, but this is how the standard library does lower_bounds


```cpp
while (l < r) {
	Integer m = l + (r - l) / 2; // prefer std::midpoint in C++20
	if (isFalse(m)) {
		l = m + 1;
	} else {
		r = m;
	}
}
return r;
```

### Qs
<<https://leetcode.com/problems/binary-search>>
Just simple binary search

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0;
        int r = nums.size()-1;
        while(l <= r){
            int pivot = (l+r)/2;
            if (nums[pivot] == target) {
                return pivot;
            }
            else if (nums[pivot] > target) {
                r = pivot-1;
            }
            else {
                l = pivot+1;
            }
        }
        return -1;
    }
};
```
<<https://leetcode.com/problems/search-a-2d-matrix/description>>
Just simple binary search

```cpp
class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int l = 0;
        int r = (matrix.size() * matrix[0].size()) - 1;
        while(l <= r){
            int pivot = (l+r)/2;
            int a = pivot % matrix[0].size();
            int b = pivot / matrix[0].size();
            if (matrix[b][a] == target) {
                return true;
            }
            else if (matrix[b][a] > target) {
                r = a + (b * matrix[0].size()) -1;
            }
            else {
                l = a + (b * matrix[0].size()) +1;
            }
        }
        return false;
    }
};
```

<<https://leetcode.com/problems/koko-eating-bananas/description>>
Naive
- Intuition is that you want the sum of all piles divided by k to be equal to h

Good
- I wonde if just doing a binary search on the max in the array and 1 for k, then just going through the piles is actually the solution. Thats nlogn, 1 space, which kinda fits?

```cpp
class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int m = 0;
        for(int i = 0 ; i < piles.size(); i++){
            m = max(m,piles[i]);
        }
        int l = 1;
        int r = m;
        while(l <= r){
            int pivot = (l+r)/2;
            long calc = 0;
            for(int i = 0 ; i < piles.size(); i++){
                calc += (piles[i])/pivot;
                if (piles[i]%pivot != 0) {
                    calc++;
                }
            }
            if (calc > (long)h) {
                l = pivot +1;
            }
            else {
                r = pivot - 1;
            }
        }
        return l;
    }
};
```
<<https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description>>
Naive
- Need to be careful with selecting the pivot. think through the steps of what happens when pivot is x or y. Do you need the lower bound or upper bound and how does that affect your binary search algo?

```cpp
class Solution {
public:
    int findMin(vector<int>& nums) {
        int l = 0;
        int r = nums.size()-1;
        while(l <= r){
            int pivot = (l+r)/2;
            if(nums[l] > nums[pivot] ){// min is left side or pivot is min
                r = pivot;
            }
            else if (nums[pivot] >= nums[r]) {//pivot is right side
                l = pivot +1;
            }
            else {// no pivot?
                r = pivot-1;
            }
        }
        int ans = INT_MAX;
        if (l >= 0 && l < nums.size()) {
            ans = min(ans,nums[l]);
        }
        if (r >= 0 && r < nums.size()) {
            ans = min(ans,nums[r]);
        }
        return ans;
    }
};
```
<<https://leetcode.com/problems/search-in-rotated-sorted-array/description>>
Good
- Keep it simple stupid
- Just think step by step on the base case, don't be too quick and copy just think through an example step by step, that is all you need

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int l = 0;
        int r = nums.size()-1;
        while(l <= r){
            int pivot = (l+r)/2;
            if(nums[pivot] == target) return pivot;
            //left sorted
            if (nums[l] < nums[pivot]) {
                if(nums[pivot] > target) {
                    if(nums[l] > target) {
                        if(nums[l] == target) return l;
                        l = pivot + 1;
                    } else {
                        if(nums[r] == target) return r;
                        r = pivot -1;
                    }
                } else {
                    if(nums[l] == target) return l;
                    l = pivot + 1;
                }
            }
            else { // right sorted
                if (nums[pivot] > target){
                    if(nums[r] == target) return r;
                    r = pivot -1;
                } else {
                    if (nums[r] > target) {
                        if(nums[l] == target) return l;
                        l = pivot +1;
                    } else {
                        if(nums[r] == target) return r;
                        r = pivot -1;
                    }
                }
            }
        }
        return -1;
    }
};
```


<<https://leetcode.com/problems/time-based-key-value-store/description>>
Naive
- Initial impression is that we'd like something that works like a hashmap
- But also preserves timestamp order (with the corresponding timestamp value)
- Two options ordering at the top then to have the hashing or have the hashing at the top then the ordering. Like hashing at the top pointing to something that maintains the ordering.

Good
- Now the question is what is the thing that preserves ordering
- ordered thing can have log n insert time. so set and get will both have log n time, and n space
- This ordered structure is likely a map 
- map is sorted by keys by default. Can use find to find a value.

```cpp
class TimeMap {
public:
    unordered_map<string, map<int, string>> mp;
    TimeMap() {}
    
    void set(string key, string value, int timestamp) {
        mp[key][timestamp] = value; 
    }
    
    string get(string key, int timestamp) {
        if(!mp.count(key)) return "";

        // find greatest that isnt target > k
        auto it = mp[key].upper_bound(timestamp);

        // find largest valid value <= k
        if(it != mp[key].begin()) it--;
        auto kv = (*it);
        if (kv.first > timestamp) return "";
        return kv.second;
    }
};
```

<<https://leetcode.com/problems/median-of-two-sorted-arrays/description>>
Naive
- I need something ordered to combine the two arrays, then after i've done the insertions I could to a find.
- Issue with this solution is it is likely going to be nlogn
- Pass through and insert into data structure seem unlikely as at a base that will be n+m

Good
- at any index of the array, I know how many are larger and how many are less
