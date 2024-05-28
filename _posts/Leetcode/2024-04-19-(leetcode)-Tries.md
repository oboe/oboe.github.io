<https://leetcode.com/problems/implement-trie-prefix-tree>
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
            //cout < c <":" < found < "\n";
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
<https://leetcode.com/problems/design-add-and-search-words-data-structure>
Naive
- Same as above
- Read the question


```cpp
class Node{
    public:
        char val;
        bool end;
        vector<Node*> nexts;
        Node(char c){
            val = c;
            end = false;
        }
};

class WordDictionary {
public:
    Node* head;
    WordDictionary() {
        head = new Node('#');
    }
    
    void addWord(string word) {
        Node* curr = head;
        for(char c  : word){
            bool found = false;
            for(Node* n : curr->nexts){
                if(n->val == c){
                    found = true;
                    curr = n;
                }
            }
            if(!found){
                Node* newNode = new Node(c);
                curr->nexts.push_back(newNode);
                curr = newNode;
            }
        }
        curr->end = true;
    }
    
    bool search(string word) {
        return search(word, head);
    }

    bool search(string word, Node* root) {
        if(!root) return false;
        if(word.size() == 0 && root->end) return true;
        if(word.size() == 0) return false;
        char first = word[0];
        string remaining = word.substr(1);
        bool ans = false;
        if(first == '.'){
            for(Node* n : root->nexts){
                if(remaining.size() == 0 && n->end){
                    return true;
                }
                ans = ans || search(remaining, n);
            }
        }
        else{
            for(Node* n : root->nexts){
                if(n->val == first) {
                    if(remaining.size() == 0 && n->end){
                        return true;
                    }
                    ans = ans || search(remaining, n);
                }
            }
        }
        return ans;
    }
};
```
<https://leetcode.com/problems/word-search-ii>
Naive
- generate every single word from the grid
- optimisation could be to just hash every single sub word so i can exist early when i try generate every single word
- Main question is how expensive is that then

Good
- trie
- don;t create new structures, you're doing dfs, passing through state, makes it faster!

```cpp
class Node{
    public:
        char val;
        bool end;
        string word;
        unordered_map<char,Node*> nexts;
        Node(char c){
            val = c;
            end = false;
            word = "";
        }
};

class Solution {
public:
    int wordsSize;
    vector<string> findWords(vector<vector<char>& board, vector<string>& words) {
        Node* root = new Node('#');

        //add all words to trie
        //prune possible words
        wordsSize = 0;
        unordered_map<char,int> mp;
        for(int i = 0 ; i < board.size() ;i++){
            for(int j = 0 ; j < board[0].size() ; j++){
                mp[board[i][j]]++;
            }
        }
        for(string word: words){
            unordered_map<char,int> mpp;
            for(char c : word){
                mpp[c]++;
            }
            bool possible = true;
            for(auto a:mpp){
                if(!mp[a.first] || mp[a.first] < a.second){
                    possible = false;
                }
            }
            if(possible){
                wordsSize++;
                addWord(word,root);
                cout < word < "\n";
            }
        }

        //iterate through all starting indexes ans start a search
        unordered_set<string> ans;
        for(int i = 0 ; i < board.size() ;i++){
            for(int j = 0 ; j < board[0].size() ; j++){
                set<pair<int,int> visited;
                search(i,j,visited,board,ans,root);
            }
        }

        //iterate through set into ans vector
        vector<string> finalAns;
        for(string s : ans){
            finalAns.push_back(s);
        }
        return finalAns;
    }

    void addWord(string word, Node* input){
        Node* curr = input;
        for(char c : word){
            if(curr->nexts[c]){
                curr = curr->nexts[c];
            }
            else{
                curr->nexts[c] = new Node(c);
                curr = curr->nexts[c];
            }
        }
        curr->end = true;
        curr->word = word;
    }

    void search(int x, int y, set<pair<int,int>& visited, vector<vector<char>& board, unordered_set<string>& ans, Node* curr){
        if(ans.size() == wordsSize) return;
        if(visited.count(make_pair(x,y)) !=0) return;
        if(x<0 || x >= board.size()) return;
        if(y<0 || y >= board[0].size()) return;
        char currentChar = board[x][y];
        if(!curr->nexts[currentChar]) return;
        visited.insert(make_pair(x,y));
        if(curr->nexts[currentChar]->end){
            ans.insert(curr->nexts[currentChar]->word);
        }
        search(x+1,y,visited,board,ans,curr->nexts[currentChar]);
        search(x-1,y,visited,board,ans,curr->nexts[currentChar]);
        search(x,y+1,visited,board,ans,curr->nexts[currentChar]);
        search(x,y-1,visited,board,ans,curr->nexts[currentChar]);
        visited.erase(make_pair(x,y));
    }
};
```