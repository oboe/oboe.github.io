<https://leetcode.com/problems/implement-trie-ii-prefix-tree/description/>
Naive
- standard implement a trie structure
- constructor will create a dummy head node
- insert, will iterate down the tree adding children when necessary
- countWordsEqualTo, iterates down the tree and returns the count at the node
- countWordsStartingWith, iterates down the tree and returns number of words that overlap
- erase goes down tree as we'd expect
- so trie needs two integers. One for standard usage, other to be accumulated for end of word

```cpp
class Node {
public:
    char c;
    vector<Node*> children;
    int usage;
    int ends;
    Node(char ch) {
        c = ch;
        usage = 0;
        ends = 0;
    }
};

class Trie {
public:
    Node* head;
    Trie() {
        head = new Node('#');
    }
    
    void insert(string word) {
        Node* curr = head;
        for(char c : word){
            bool found = false;
            for(Node* n: curr->children){
                if(n->c == c){
                    found = true;
                    curr = n;
                }
            }
            if(!found) {
                Node* newNode = new Node(c);
                curr->children.push_back(newNode);
                curr = newNode;
            }
            curr->usage++;
        }
        curr->ends++;
    }
    
    int countWordsEqualTo(string word) {
        Node* curr = head;
        for(char c : word){
            bool found = false;
            for(Node* n: curr->children){
                if(n->c == c) {
                    found = true;
                    curr = n;
                }
            }
            if(!found) return 0;
        }
        return curr->ends;
    }
    
    int countWordsStartingWith(string prefix) {
        Node* curr = head;
        for(char c : prefix){
            bool found = false;
            for(Node* n: curr->children){
                if(n->c == c) {
                    found = true;
                    curr = n;
                }
            }
            if(!found) return 0;
        }
        return curr->usage;
    }
    
    void erase(string word) {
        Node* curr = head;
        for(char c : word){
            bool found = false;
            for(Node* n: curr->children){
                if(n->c == c) {
                    found = true;
                    curr = n;
                }
            }
            if(!found) return;
            curr->usage--;
        }
        curr->ends--;
    }
};

/**
 * Your Trie object will be instantiated and called as such:
 * Trie* obj = new Trie();
 * obj->insert(word);
 * int param_2 = obj->countWordsEqualTo(word);
 * int param_3 = obj->countWordsStartingWith(prefix);
 * obj->erase(word);
 */
```

<https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/>
Naive
- need to choose one day to buy stock and another to sell
- naive is just go through every i,j position and calculate the profit

Good
- single pass, maintain a min and update a best profit at each point.

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

<https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/>
Naive
- Just recursively choose a transaction to make profit on.

Good
- just sum up all the diffs

```cpp
class Solution {
    // [7,1,5,3,6,4]
    //  [0,4,0,3,0]
public:
    int maxProfit(vector<int>& prices) {
        if (prices.size() == 0){
            return 0;
        }
        int profit = 0;
        int last = prices[0];
        for(int i = 1 ; i < prices.size() ; i++){
            int curr = prices[i];
            if(curr > last){
                profit += curr - last;
            }
            last = curr;
        }
        return profit;
    }
};
```


<https://leetcode.com/problems/lfu-cache/description/>
Naive
- just have a key to count map, and each insertion update this count and do a n time pass to evict the least recently used key
- So a hashmap
- map for count to keys, and maintaining min count so far seems like a good idea

Good
```cpp
class LFUCache {
public:
    unordered_map<int, list<pair<int,int>>> frequencies;
    // key : 
    unordered_map<int, pair<int,list<pair<int,int>>::iterator>> cache;
    int capacity;
    int minf;
    LFUCache(int capacity) : capacity(capacity), minf(0) {}

    void insert(int key, int frequency, int value) {
        frequencies[frequency].push_back({key,value});
        cache[key] = {frequency, --frequencies[frequency].end()}; //insert iterator to last elem
    }
    
    int get(int key) {
        auto it = cache.find(key);
        if(it == cache.end()) return -1;
        int f = it->second.first;
        auto iter = it->second.second;
        pair<int,int> kv = *iter; // {key,value}

        //remove existing key val
        frequencies[f].erase(iter);
        if(frequencies[f].empty()) {
            frequencies.erase(f);
            if(minf == f) minf++; // feels jank, is this guarenteed to be true?
        }

        insert(key, f+1, kv.second); // insert key val with 1 more frequency
        return kv.second;
    }
    
    void put(int key, int value) {
        if(capacity <= 0) return;
        auto it = cache.find(key); //{freq,it{k,v}}
        if(it != cache.end()){//found
            it->second.second->second = value;
            get(key);
            return;
        }
        if(capacity == cache.size()){
            cache.erase(frequencies[minf].front().first);
            frequencies[minf].pop_front();

            if(frequencies[minf].empty()) {
                frequencies.erase(minf);
            }
        }
        minf = 1;
        insert(key,1,value);
    }


};

/**
 * Your LFUCache object will be instantiated and called as such:
 * LFUCache* obj = new LFUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
```

<https://leetcode.com/problems/wildcard-matching/description/>
Naive
- If there was only the ? then you could just do a simple pass and compare char by char
- now with the * we need to handle case where string will match as many characters as possible and we can continue our search without the * char.
- recursively search if it's a match character by character

```cpp
# Naive just topdown memoize
# inefficient substrs
class Solution {
public:
    unordered_map<string,unordered_map<string,bool>> StoPtoVal;
    bool isMatch(string s, string p) {
        //cout << s << " : " << p << "\n";
        if(StoPtoVal.count(s) != 0){
            if(StoPtoVal[s].count(p)){
                return StoPtoVal[s][p];
            }
        }
        if(s.size() == 0 && p.size() == 0 ) return true;
        if(s.size() == 0 || p.size() == 0){
            bool allStar = true;
            for(char c : s){
                if(c != '*') allStar = false;
            }
            for(char c : p){
                if(c != '*') allStar = false;
            }
            StoPtoVal[s][p] = allStar;
            return allStar;
        }
        char a  = s[0];
        char b = p[0];
        if(a == b || a == '?' || b == '?') {
            string aa = "";
            string bb = "";
            if(s.size()-1 != 0) aa = s.substr(1,s.size()-1);
            if(p.size()-1 != 0) bb = p.substr(1,p.size()-1);
            bool match = isMatch(aa,bb);
            StoPtoVal[s][p] = match;
            return match;
        }
        if(a != '*' && b != '*') return false;
        bool matched = false;
        if(a == '*'){
            for(int i = 0 ; i < p.size() ;i++){
                string aa = "";
                string bb = "";
                if(s.size()-1 != 0) aa = s.substr(1,s.size()-1);
                if(p.size()-i != 0) bb = p.substr(i,p.size()-i);
                bool match = isMatch(aa,bb);
                StoPtoVal[s][p] = match;
                matched |= match;
                if(matched) return true;
            }
            string aa = "";
            if(s.size()-1 != 0) aa = s.substr(1,s.size()-1);
            bool match = isMatch(aa,"");
            StoPtoVal[s][""] = match;
            matched |= match;
            if(matched) return true;
        }
        if(b == '*'){
            for(int i = 0 ; i < s.size() ;i++){
                string aa = "";
                string bb = "";
                if(s.size()-i != 0) aa = s.substr(i,s.size()-i);
                if(p.size()-1 != 0) bb = p.substr(1,p.size()-1);
                bool match = isMatch(aa,bb);
                StoPtoVal[s][p] = match;
                matched |= match;
                if(matched) return true;
            }
            string bb = "";
            if(p.size()-1 != 0) bb = p.substr(1,p.size()-1);
            bool match = isMatch("",bb);
            StoPtoVal[""][p] = match;
            matched |= match;
            if(matched) return true;
        }
        StoPtoVal[s][p] = false;
        return false;
    }
};
```

```cpp
class Solution {
public:
    // f(i,j) = f(i-1,j-1) && (s[i] == p[i]) STANDARD
    // f(i,j) =  MATCH NOTHING
    // f(i,j)ALREADY MATCHED SOMETHING
    bool isMatch(string s, string p) {
        vector<vector<bool>> dp(s.size()+1,vector<bool>(p.size()+1,false));
        dp[0][0] = true;
        for(int j = 0 ; j < p.size() ;j++){
            if(p[j] == '*') dp[0][j+1] = dp[0][j+1] |dp[0][j];
        }
        for(int i = 0 ; i < s.size() ;i++){
            if(s[i] == '*') dp[i+1][0] = dp[i+1][0] |dp[i][0];
        }
        for(int i = 0 ; i < s.size() ; i++){
            for(int j = 0 ; j < p.size() ;j++){
                char a = s[i];
                char b = p[j];
                if(charMatch(a,b)) dp[i+1][j+1] = dp[i+1][j+1] | dp[i][j];
                if(a == '*' || b=='*'){
                    dp[i+1][j+1] = dp[i+1][j+1] |dp[i+1][j];
                    dp[i+1][j+1] = dp[i+1][j+1] |dp[i][j+1];
                }
            }
        }
        return dp[s.size()][p.size()];
    }

    bool charMatch (char a, char b) {
        if(a == '?' || a == '*' || b == '?' || b == '*') return true;
        return (a==b);
    }
};
```
<https://leetcode.com/problems/regular-expression-matching/description/>
Naive
- No star, simple pass
- we can recursively compute the answer popping the top char
- for the star we can just go through all the options. doing a search if it matches zero, if it matches 1, etc
- of course we can just cache these intermediate results, between trees
- now we can notice that this caching is actually just computing suffixes of the two strings. So we only need to know the i,j values to cache
- We can actually store these results in a 2d grid and compute it bottom up. Lets us avoid dealing with stack limits
- 


<https://leetcode.com/problems/basic-calculator/description/>

<https://leetcode.com/problems/broken-calculator/description/>

<https://leetcode.com/problems/basic-calculator-ii/description/>

<https://leetcode.com/problems/basic-calculator-iii/>

<https://leetcode.com/problems/basic-calculator-iv/description/>

