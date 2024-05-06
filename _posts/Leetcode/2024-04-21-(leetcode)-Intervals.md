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

https://leetcode.com/problems/non-overlapping-intervals/

https://leetcode.com/problems/minimum-interval-to-include-each-query/

