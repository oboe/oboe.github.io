## Context
Greedy algorithms exploit the fact that a locally optimal choice is also globally optimal. The hard part is getting the intuition on the correctness. A good thing to do is to solve the base cases to try build intuition on if what is locally optimal is globally optimal.

#### Interval scheduling.
1. If provided a list of starting and ending time intervals, try to pack the max amount of intervals.
2. Just iterating by starting time and prioritising the interval that ends as early is possible is actually optimal.
3. Intuition is that it's always better to pack with a interval ending earlier.

#### Tasks and deadlines
1. Provided list of tasks with durations and deadlines you want to maximise payoff which is d-x, x being the time you complete a task
2. Just prioritising shorter durations is optimal
3. Can build intuition by solving a 2 task case

## Qs
<https://leetcode.com/problems/maximum-subarray>
Naive
- Taking all i,j positions, n^2

Good
- intuition that  max subarray ending in position B, must be included for a subarray in position B+1. This is the recursive relation here.

```cpp
class Solution {
    // simple n^2 solution
    // [a,b,c]
    // good
    // m(a,b+1) = max(0,m(a,b)) + b+1
public:
    int maxSubArray(vector<int>& nums) {
        int best = nums[0];
        int prevSubStringSum = 0;
        for(int i = 0 ; i < nums.size();i++){
            int curr = max(0,prevSubStringSum) + nums[i];
            best = max(best,curr);
            prevSubStringSum = curr;
        }
        return best;
    }
};
```

<https://leetcode.com/problems/jump-game>
Naive
- Return if last is reachable
- Go through every index, flag the next points we can reach
- If the index we're on is a reachable point then reupdate next points we can reach
- key point to consider is that we only need to care about the max position we can reach

```cpp
class Solution {
public:
    bool canJump(vector<int>& nums) {
        int maxReachable = 0;
        for(int i = 0 ; i < nums.size();i++){
            if(i <= maxReachable){
                maxReachable = max(maxReachable, i+nums[i]);
            }
        }
        return (maxReachable >= nums.size()-1);
    }
};
```

<https://leetcode.com/problems/jump-game-ii>
Naive
- return number of minimum jumps
- Go through each index, paint vector with min jumps to reach
- Doing this would be a n*k

Good
- Is there any way we can improve this?
- You can also do a BFS like solution where all reachable positions are a level in the tree. And you process level by level.

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        vector<int> jumps(nums.size(),INT_MAX);
        jumps[0] = 0;
        for(int i = 0 ; i < nums.size() ;i++){
            for(int j = 1 ; j <= nums[i];j++){
                if(i+j >= nums.size()) break;
                jumps[i+j] = min(jumps[i+j],jumps[i]+1);
            }
        }
        return jumps[jumps.size()-1];
    }
};
```

<https://leetcode.com/problems/gas-station>
Naive
- Go through every index and try to find out if I can do a loop
- Is there any way I can share the compute of previous calculations here?
- I understand that at the end of the day each gas station either adds gas or reduces gas, just diff the cost from the gas

Good
- my conclusion is that greedy questions are often just adhoc, and require an insight that you'd like yo prove but is quite hard to do
- 

```cpp
class Solution {
public:
    int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
        if(accumulate(gas.begin(),gas.end(),0) < accumulate(cost.begin(),cost.end(),0)){
            return -1;
        }
        int startPos = 0;
        int sum =0;
        for(int i = 0 ; i  < gas.size();i++){
            sum += gas[i] - cost[i];
            if(sum < 0) {
                sum = 0;
                startPos = i+1;
            }
        }
        return startPos;
    }
};
```

<https://leetcode.com/problems/hand-of-straights>
Naive
- Verify if array can be split into k groups of consecutive numbers
- As they want straights thinking that maybe I'd like some kind of ordering to help me here
- I've sorted and then gone through greedily assigning results
- Believe my solution is actually n^2

```cpp
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if(hand.size()%groupSize != 0) return false;
        sort(hand.begin(),hand.end());
        vector<pair<int,int> valueSizePairs;
        for(int i = 0 ; i < hand.size();i++){
            bool placed = false;
            for(int j = 0;j < valueSizePairs.size();j++){//find hand to place on
                if(valueSizePairs[j].second != groupSize && valueSizePairs[j].first == hand[i]-1){
                    valueSizePairs[j].first++;
                    valueSizePairs[j].second++;
                    placed = true;
                    break;
                }
            }
            if(!placed){
                valueSizePairs.push_back({hand[i],1});
            }
        }
        return (valueSizePairs.size() == hand.size()/groupSize);
    }
};
```

Good
- Use an ordered map for frequencies then pass through each index hand like that

```cpp
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int groupSize) {
        if(hand.size()%groupSize != 0) return false;
        map<int,int> freq;
        for(int i : hand){
            freq[i]++;
        }
        for(auto a: freq){
            if(a.second == 0) continue;
            if(a.second > hand.size()/groupSize) return false;
            for(int i = 0 ; i < groupSize; i++){
                if(freq[a.first+i]-a.second < 0) return false;
                freq[a.first+i] = freq[a.first+i]-a.second;
            }
        }
        return true;
    }
};
```

<https://leetcode.com/problems/merge-triplets-to-form-target-triplet>
Naive
- Feels like just finding max possible by doing a pass, pruning invalid triplets
- then at end compare if its our target

```cpp
class Solution {
public:
    bool mergeTriplets(vector<vector<int>& triplets, vector<int>& target) {
        vector<int> best(3);
        for(vector<int> triplet: triplets){
            if(triplet[0] > target[0] || triplet[1] > target[1] || triplet[2] > target[2]) continue;
            best[0] = max(best[0], triplet[0]);
            best[1] = max(best[1], triplet[1]);
            best[2] = max(best[2], triplet[2]);
        }
        return (best[0] == target[0] && best[1] == target[1] && best[2] == target[2]);
    }
};
```

<https://leetcode.com/problems/partition-labels>
Naive
- Each letter has a min range, and overlapping ranges need to be merged
- Pass to get min max for each letter
- iterate through min max combining to get list of non overlapping intervals
- return that

```cpp
class Solution {
public:
    vector<int> partitionLabels(string s) {
        //create min max intervals for each letter
        unordered_map<char,pair<int,int> charsToMinMaxPair;
        for(int i = 0 ;i < s.size() ;i++){
            if(charsToMinMaxPair.count(s[i]) == 0){
                charsToMinMaxPair[s[i]] = make_pair(i,i);
            }
            else{
                charsToMinMaxPair[s[i]] = make_pair(min(charsToMinMaxPair[s[i]].first,i),i);
            }
        }
        vector<int> ans;
        //create vector of intervals
        vector<pair<int,int> intervals;
        for(auto a : charsToMinMaxPair){
            intervals.push_back(a.second);
        }
        //merge intervals
        sort(intervals.begin(),intervals.end());
        pair<int,int> curr = intervals[0];
        for(int i = 1 ; i < intervals.size();i++){
            if(curr.second < intervals[i].first){//non overlapping
                ans.push_back(curr.second-curr.first+1);
                curr = intervals[i];
            } else{
                curr.first = min(curr.first,intervals[i].first);
                curr.second = max(curr.second,intervals[i].second);
            }
        }
        ans.push_back(curr.second-curr.first+1);
        return ans;
    }
};
```

Good
- Find out last occurence of each character
- Iterate through array, updating a pointer on last valid index. When the index we're at is equal to the last valid index then thats a partition. If its not the last index, kick back the pointer to the last one and move to the next character.

<https://leetcode.com/problems/valid-parenthesis-string>
Naive
- Asking to verify if a character is valid
- Key point is that it allows asterix which can be any character
- Basic handling of parenthesis would be maintaining a stack, but how do we handle the asterix?
- We could permute all options for the characters but that would be 3^n

Good
- Thinking of just using a deque, treating it as a stack for the fast half then doing a second iteration where I pop from front and back
- But in reality stack is only needed if you have multiple parenthesis, if you have one you just need to maintain a single number, how many parenthesis you have!
- Just maintain a min and max left parenthesis you could have.

```cpp
class Solution {
public:
    bool checkValidString(string s) {
        int low = 0;
        int high = 0;
        for(char c : s){
            if(c == '*'){
                low = max(0,low-1);
                high++;
            } else if (c =='('){
                low++;
                high++;
            } else { // ')'
                low = max(0,low-1);
                high--;
                if (high<0) return false;
            }
        }
        return low==0;
    }
};
```