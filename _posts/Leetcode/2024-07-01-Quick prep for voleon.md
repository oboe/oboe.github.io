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
- get,put apis
- we need to track the number of things each key has
- get and put needs constant
- on basics, simple get, put of values could be handled by a hashmap
- Naive would be just maintain a hashmap mapping keys to use counter and iterate through all keys to get 

Good
- now the question is how to handle the eviction
- feels like a pqueue, min heap would be best here, to let us maintain the smallest element to pop.
- Now the question is how can I maintain both together?
- I usually like having my pqueues be over vectors, but im pretty sure I can continue to use a deque, so this means that when I add elements it wont dereference previous pointers I have, which is nice.


<https://leetcode.com/problems/wildcard-matching/description/>
Naive
- just on first look 


<https://leetcode.com/problems/regular-expression-matching/description/>

<https://leetcode.com/problems/basic-calculator/description/>

<https://leetcode.com/problems/broken-calculator/description/>

<https://leetcode.com/problems/basic-calculator-ii/description/>

<https://leetcode.com/problems/basic-calculator-iii/>

<https://leetcode.com/problems/basic-calculator-iv/description/>