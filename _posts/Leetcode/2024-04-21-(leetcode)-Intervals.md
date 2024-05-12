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
- 2^n complexity
- Main thinking go through sorted version and when i find out a and be are colliding remove one and continue. Main issue is that i need to choose between which one to remove here and both could be valid options.

Good
- What would a good solution look like?
- solution is greedy
- Sort and sequentially compare adjacent intervals
- Greedily prioritise removing the intervals which would most negatively impact us: those with a larger ending point.

```cpp
class Solution {
public:
    int eraseOverlapIntervals(vector<vector<int>>& intervals) {
        sort(intervals.begin(),intervals.end());
        if(intervals.size() <= 1){
            return 0;
        }
        //track last interval end
        int lastEnd = max(INT_MIN, intervals[0][1]);
        int ans = 0;
        for(int i = 1 ; i < intervals.size() ; i++){
            if(lastEnd <= intervals[i][0]){ //not overlapping
                lastEnd = intervals[i][1];
            } else { //overlapping
                ans++;
                //remove shorter end interval
                lastEnd = min(lastEnd, intervals[i][1]);
            }
        }
        return ans;
    }
};
```

https://leetcode.com/problems/minimum-interval-to-include-each-query/
Naive
- list of intervals
- wants queries getting the size of the smallest interval which is within a query
- length of intervals is n, number of queries is also n
- Naive approach is just for each query, doing a pass to find valid intervals and maintaining the one with the smallest one
- Definitely feels like I need to maintain something to quickly get the intervals
- Another thing I could do is sort on interval size, and leading from largest intervals paint the 10^7 range with the relevant interval
- interesting call out is they are not asking for the interval index, they are asking for the interval size

Good
