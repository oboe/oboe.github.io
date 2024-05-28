<https://leetcode.com/problems/kth-largest-element-in-a-stream>
Naive
- hmm need something to maintain ordering
- Initial impression is a pqueue or a multiset
- pqueue you can only access top element, so use multiset instead

Good
- Key point is that use pqueue to maintain max or min k elements
- pqueue can only have fast access to the top so keep that in mind

```cpp
class KthLargest {
public:
	// makes it a min pqueue aka smallest element on the top
    priority_queue<int,vector<int>, greater<int> pq;
    int size;
    KthLargest(int k, vector<int>& nums) {
        size = k;
        for(int i : nums){
            add(i);
        }
    }
    
    int add(int val) {
        pq.push(val);
        while(pq.size() > size){
            pq.pop();
        }
        return pq.top();
    }
};
```

<https://leetcode.com/problems/last-stone-weight>
This time it's a max heap.

```cpp
class Solution {
public:
    int lastStoneWeight(vector<int>& stones) {
        priority_queue<int> maxHeap;
        for(int i : stones){
            maxHeap.push(i);
        }
        while(maxHeap.size() >= 2){
            int a = maxHeap.top();
            maxHeap.pop();
            int b = maxHeap.top();
            maxHeap.pop();
            if(a == b) continue;
            if(a > b){
                maxHeap.push(a-b);
            }
            else{
                maxHeap.push(b-a);
            }
        }
        if(maxHeap.empty()) return 0;
        return maxHeap.top();
    }
};
```
<https://leetcode.com/problems/k-closest-points-to-origin>
Naive: 
- Ask yourself what do you need
- Do you need a min heap or a max heap?
- Do you need the k smallest things at the end?
- Do you need the kth smallest thing each time?

```cpp
class Solution {
public:
    vector<vector<int> kClosest(vector<vector<int>& points, int k) {
        priority_queue<pair<float,int> pqDistIndex;
        for(int i = 0 ; i < points.size();i++){
            float x = points[i][0];
            float y = points[i][1];
            float ans = sqrt(x*x + y*y);
            cout < ans < " "<x < " " < y < "\n";
            pqDistIndex.push(make_pair(ans,i));
        }
        while(pqDistIndex.size() > k ){
            pqDistIndex.pop();
        }
        vector<vector<int> ans;
        while(!pqDistIndex.empty()){
            ans.push_back(points[pqDistIndex.top().second]);
            pqDistIndex.pop();
        }
        return ans;
    }
};
```

<https://leetcode.com/problems/kth-largest-element-in-an-array>
Naive
- Need something which maintains ordering
- Likely a p queue
- As I need the kth largest element I want to pop off the smaller elements quickly so I need a min heap

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        priority_queue<int, vector<int>, greater<int> pq;
        for(int i : nums){
            pq.push(i);
            if (pq.size() > k) pq.pop();
        }
        return pq.top();
    }
};
```

<https://leetcode.com/problems/task-scheduler>
Naive
- identical tasks must be separated by at least n intervals due to cooling time.
- Return the minimum number of intervals required to complete all tasks
- initial impression is that i need to just prioritise doing the task with the most duplicates when possible
- So as i need to pop the max, i need a max heap
- How can I maintain the cool down period?

Good
- nlogn, n space

```cpp
class Solution {
public:
    int leastInterval(vector<char>& tasks, int n) {
        priority_queue<pair<int,char> pq;
        int cooldownSize = 0;
        vector<pair<int,char> pairToCooldown(n+1);
        int cycles = 0;
        //insert tasks
        unordered_map<char,int> singleUseMap;
        for(char c : tasks){
            singleUseMap[c]++;
        }
        for(auto a : singleUseMap){
            pq.push(make_pair(a.second,a.first));
        }
        while(!pq.empty() || cooldownSize != 0){
            cycles++;
            //update and pop from cooldown area
            if(pairToCooldown[0].first != 0){
                pq.push(pairToCooldown[0]);
                cooldownSize--;
            }
            for(int i = 1 ;i < pairToCooldown.size() ; i++){
                pairToCooldown[i-1] = pairToCooldown[i];
            }
            pairToCooldown[n] = make_pair(0,'#');
            //pop max
            if(!pq.empty()){
                pair<int,char> val = pq.top();
                pq.pop();
                if (val.first == 1) continue;
                pairToCooldown[n] = make_pair(val.first-1,val.second);
                cooldownSize++;
            }
        }
        return cycles;
    }
};
```

<https://leetcode.com/problems/design-twitter>
Naive
- 10 most recent tweet ids
- Each user maintains a min heap, with timestamp,tweetid pairs

```cpp
class Twitter {
public:
    unordered_map<int,set<int> userToFollows;
    unordered_map<int,priority_queue<pair<int,int>,vector<pair<int,int>,greater<pair<int,int>> userTweets;
    int time;
    Twitter() {
        time = 0;
    }
    
    void postTweet(int userId, int tweetId) {
        userTweets[userId].push({time,tweetId});
        if(userTweets[userId].size() > 10) userTweets[userId].pop();
        time++;
    }
    
    vector<int> getNewsFeed(int userId) {
        priority_queue<pair<int,int> pq;
        addTweets(pq,userId);
        for(auto a: userToFollows[userId]){
            addTweets(pq,a);
        }
        int i = 0;
        vector<int> ans;
        while(!pq.empty()){
            ans.push_back(pq.top().second);
            pq.pop();
            i++;
            if(i==10) break;
        }
        return ans;
    }

    void addTweets(priority_queue<pair<int,int>& pq, int userId){
        vector<pair<int,int> temp;
        while(!userTweets[userId].empty()){
            pair<int,int> top = userTweets[userId].top();
            userTweets[userId].pop();
            pq.push(top);
            temp.push_back(top);
        }
        for(auto a: temp){
            userTweets[userId].push(a);
        }
    }
    
    void follow(int followerId, int followeeId) {
        userToFollows[followerId].insert(followeeId);
    }
    
    void unfollow(int followerId, int followeeId) {
        userToFollows[followerId].erase(followeeId);
    }
};
```

<https://leetcode.com/problems/find-median-from-data-stream>
Naive
- 

Good
- Maintain a max heap and a min heap

```cpp
class MedianFinder {
public:
    priority_queue<int,vector<int>,greater<int> minHeap;//top
    priority_queue<int> maxHeap;//bottom
    MedianFinder() {}
    
    void addNum(int num) {
        if(maxHeap.empty()){
            minHeap.push(num);
        } else if (minHeap.empty()){
            maxHeap.push(num);
        } else if(maxHeap.top() > num){
            maxHeap.push(num);
        } else{
            minHeap.push(num);
        }
        rebalance();
    }

    void rebalance(){
        while(abs((double)(minHeap.size() - maxHeap.size())) > 1.0 ){
            if(minHeap.size() > maxHeap.size()){
                maxHeap.push(minHeap.top());
                minHeap.pop();
            }else{
                minHeap.push(maxHeap.top());
                maxHeap.pop();
            }
        }
    }
    
    double findMedian() {
        if(minHeap.size() == maxHeap.size()){
            double ans = ((double)(minHeap.top() + maxHeap.top()))/2.0;
            return ans;
        } else if(minHeap.size() > maxHeap.size()){
            return (double)(minHeap.top());
        }
        else{
            return (double)(maxHeap.top());
        }
    }
};
```