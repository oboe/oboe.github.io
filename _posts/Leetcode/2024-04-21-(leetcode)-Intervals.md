https://leetcode.com/problems/insert-interval/
Naive
- insert an interval so its non overlapping
- iterate through array, if non overlapping push to ans vector
- if overlapping log left of overlapping array then combine 
- n complexity, n space

```cpp
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> ans;
        bool inserted = false;
        for(int i = 0 ; i < intervals.size() ;i++){
            vector<int> curr = intervals[i];
            if(curr[1] < newInterval[0]){//non overlapping
                ans.push_back(curr);
                continue;
            }
            if(newInterval[1] < curr[0]){
                if(!inserted) ans.push_back(newInterval);
                ans.push_back(curr);
                inserted = true;
                continue;
            }
            newInterval[0] = min(newInterval[0],curr[0]);
            newInterval[1] = max(newInterval[1],curr[1]);
        }
        if(!inserted) ans.push_back(newInterval);
        return ans;
    }
};
```
https://leetcode.com/problems/merge-intervals/

```cpp
class Solution {
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(),intervals.end());
        if(intervals.size()==0) return intervals;
        vector<vector<int>> ans;
        vector<int> curr = intervals[0];
        for(int i = 1 ;i <intervals.size(); i++){
            if(curr[1]< intervals[i][0]){//non overlapping
                ans.push_back(curr);
                curr = intervals[i];
                continue;
            } else{
                curr[0] = min(curr[0],intervals[i][0]);
                curr[1] = max(curr[1],intervals[i][1]);
            }
        }
        ans.push_back(curr);
        return ans;
    }
};
```

https://leetcode.com/problems/non-overlapping-intervals/
Naive
- bad solution would be try every removal permutation and select this minimum valid one
- Main thinking go through sorted version and when i find out a and be are colliding remove one and continue. Main issue is that i need to choose between which one to remove here and both could be valid options.

https://leetcode.com/problems/minimum-interval-to-include-each-query/

