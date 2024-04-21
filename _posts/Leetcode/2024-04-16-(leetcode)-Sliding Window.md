https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
Good
- Just keep a low value

```cpp
class Solution {
    // n^2 loop
    // lowest val
public:
    int maxProfit(vector<int>& prices) {
        int best = 0;
        if (prices.size() == 0) {
            return best;
        }
        int low = prices[0];
        for(int i = 0 ; i < prices.size() ; i++){
            if(best < (prices[i] - low)){
                best = (prices[i]-low);
            }
            if(prices[i] < low){
                low = prices[i];
            }
        }
        return best;
    }
};
```


https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
Naive
- nested loop, for every start and end position 
- Just start i, and slowly increase the window until you hit 

Good 
- just instead of having two for loops, just drop the first duplicate


```cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int ans = 0;
        int l = 0;
        unordered_set<char> charSet;
        for(int i = 0 ;i < s.size() ; i++){
            if (charSet.count(s[i])) { // duplicate found!
                while(charSet.count(s[i])){
                    charSet.erase(s[l]);
                    l++;
                }
                charSet.insert(s[i]);
            }
            else {
                charSet.insert(s[i]);
                ans = max(ans, (int)charSet.size());
            }
        }
        return ans;
    }
};
```

https://leetcode.com/problems/longest-repeating-character-replacement/description/
Naive
- nested loop, for every start and end position

Good
- Sliding window, I can maintain char map, with number of duplicates
- When duplicate is above k just increment L


```cpp
class Solution {
public:
    int characterReplacement(string s, int k) {
        int ans = 0;
        int left = 0;
        int maxf = 0;
        unordered_map<char,int> charMap;
        for(int i = 0 ; i< s.size() ; i++){
            charMap[s[i]]++;

            // pop left til valid
            maxf = max(maxf, charMap[s[i]]);
            while ((i - left + 1) - maxf > k ) {
                charMap[s[left]]--;
                left++;
            }

            // get sum and update ans
            int sum = 0;
            for(auto a : charMap) {
                sum += a.second;
            }
            ans = max(ans, sum);
        }
        return ans;
    }
};
```

https://leetcode.com/problems/permutation-in-string/description/
Naive
- nested for loop. check if it is a permutation

Good
- pass s1 and create a char map
- sliding window, with isValid alarming if we exceed charmap, and at end of loop checking for complete map.

```cpp
class Solution {
public:
    bool checkInclusion(string s1, string s2) {
        unordered_map<char,int> s1Map;
        for(char c : s1){
            s1Map[c]++;
        }
        int l = 0;
        unordered_map<char,int> s2Map;
        for(int i = 0 ;i < s2.size() ; i++){
            s2Map[s2[i]]++;
            while(s2Map[s2[i]] > s1Map[s2[i]]){
                s2Map[s2[l]]--;
                l++;
            }
            int valid = true;
            for(auto a : s1Map){
                if (a.second != s2Map[a.first]) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                return true;
            }
        }
        return false;
    }
};
```

https://leetcode.com/problems/minimum-window-substring/description/
Naive: 
- nested for loop, checking if valid or not
- go through all possible substrings and check if theyre valid or not, maintaining the minimum window substring

Good
- I can pop a letter when
	- My window contains enough letters already

```cpp
class Solution {
public:
    string minWindow(string s, string t) {
        unordered_map<char, int> tMap;
        for(char c : t){
            tMap[c]++;
        }
        unordered_map<char, int> sMap;
        int l = 0;
        bool found = false;
        string ans = "";
        for(int i = 0 ;i < s.size() ; i++){
            // add right letter
            sMap[s[i]]++;

            // pop as much letters while trying to keep window valid
            while(sMap[s[l]] > tMap[s[l]]){
                if (l >= i){
                    break;
                }
                sMap[s[l]]--;
                l++;
            }

            //check if valid and update ans;
            bool valid = true;
            for(auto a: tMap){
                if (sMap[a.first] < a.second) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                if (!found || ans.size() > (i-l+1)) {
                    ans = s.substr(l,(i-l+1));
                    found = true;
                }
            }
        }
        return ans;
    }
};
```

https://leetcode.com/problems/sliding-window-maximum/description/
Naive
- nested for loop, calculate each time

Good
- Fixed size sliding window maximum, maintain sum
- maintain max using a priority queue
- p_queue won't work as pop can only remove top value
- Looks like trick is to maintain an always monotonically decreasing deque.
- Ask yourself what duplicate work can you avoid doing between the two iterations you step through
- Index issue is easily solved by keeping track of indices instead of the numbers.

Unrelated but heres how you'd define a priority queue for finding min element
```cpp
priority_queue<int,vector<int>,greater<int>> q;
```

```cpp
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int l = 0;
        vector<int> ans;
        deque<int> dq;
        for(int i = 0 ; i < nums.size() ; i++){
            if(!dq.empty() && (i - dq.front() + 1) > k ){
                dq.pop_front();
            }
            while(!dq.empty() && nums[dq.back()] < nums[i] ) {
                dq.pop_back();
            }
            dq.push_back(i);
            if(i + 1 < k){
                continue;
            }
            ans.push_back(nums[dq.front()]);
        }
        return ans;
    }
};
```