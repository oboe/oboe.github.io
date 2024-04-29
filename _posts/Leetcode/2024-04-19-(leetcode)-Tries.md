https://leetcode.com/problems/implement-trie-prefix-tree/
Naive
- Just implement a trie, I know I could make it better with a fixed array of 26 size.

```cpp
class Node{
public:
    char val;
    bool ends;
    vector<Node*> nodes;
    Node(char c){
        val = c;
        ends = false;
    }
};

class Trie {
public:
    Node* rootNode;
    Trie() {
        rootNode = new Node('#');
    }
    
    void insert(string word) {
        Node* curr = rootNode;
        for(char c : word){
            bool found = false;
            for(Node* n : curr->nodes){
                if(n->val == c){
                    found = true;
                    curr = n;
                    break;
                }
            }
            if(!found){
                Node* newN = new Node(c);
                curr->nodes.push_back(newN);
                curr = newN;
            }
        }
        curr->ends = true;
    }
    
    bool search(string word) {
        Node* curr = rootNode;
        for(char c : word){
            bool found = false;
            for(Node* n : curr->nodes){
                if(n->val == c){
                    found = true;
                    curr = n;
                    break;
                }
            }
            //cout << c <<":" << found << "\n";
            if(!found){
                return false;
            }
        }
        if(curr->ends){
            return true;
        }
        else{
            return false;
        }
    }
    
    bool startsWith(string prefix) {
        Node* curr = rootNode;
        for(char c : prefix){
            bool found = false;
            for(Node* n : curr->nodes){
                if(n->val == c){
                    found = true;
                    curr = n;
                    break;
                }
            }
            if(!found){
                return false;
            }
        }
        return true;
    }
};
```
https://leetcode.com/problems/design-add-and-search-words-data-structure/

https://leetcode.com/problems/word-search-ii/

