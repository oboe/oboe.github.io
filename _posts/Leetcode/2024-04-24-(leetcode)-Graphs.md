<https://leetcode.com/problems/number-of-islands>
Naive
- iterate through each index, starting a search
- Each search will paint all adjacents
- m,n^2

```cpp
class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int ans = 0;
        for(int i = 0 ; i < grid.size(); i++){
            for(int j = 0 ;j < grid[0].size();j++){
                if(grid[i][j] == '1') {
                    ans++;
                    paint(grid,i,j);
                }
            }
        }
        return ans;
    }

    //recursively paint all islands into water
    void paint(vector<vector<char>>& grid, int x, int y){
        if(x < 0 || x >= grid.size()) return;
        if(y < 0 || y >= grid[0].size()) return;
        if(grid[x][y] == '0') return;
        grid[x][y] = '0';
        paint(grid,x+1,y);
        paint(grid,x-1,y);
        paint(grid,x,y+1);
        paint(grid,x,y-1);
    }
};
```

<https://leetcode.com/problems/max-area-of-island>
Naive
- Just paint function which returns the value
- n^2

```cpp
class Solution {
public:
    int maxAreaOfIsland(vector<vector<int>>& grid) {
        int ans = 0;
        for(int i = 0 ; i < grid.size(); i++){
            for(int j = 0 ;j < grid[0].size();j++){
                if(grid[i][j] == 1) {
                    ans = max(ans,paint(grid,i,j));
                }
            }
        }
        return ans;
    }

    //recursively paint all islands into water
    int paint(vector<vector<int>>& grid, int x, int y){
        if(x < 0 || x >= grid.size()) return 0;
        if(y < 0 || y >= grid[0].size()) return 0;
        if(grid[x][y] == 0) return 0;
        grid[x][y] = 0;
        int ans = 1;
        ans += paint(grid,x+1,y);
        ans += paint(grid,x-1,y);
        ans += paint(grid,x,y+1);
        ans += paint(grid,x,y-1);
        return ans;
    }
};
```

<https://leetcode.com/problems/clone-graph>
Naive
- Pass through graph
- Creating an adjacency list representation, hashmap, that maps to neighbours
- Recreate each node
- Recreate all edges

```cpp
class Solution {
public:
    unordered_map<int,vector<int>> valToNeighbors;
    unordered_map<int,Node*> valToNewNode;
    Node* cloneGraph(Node* node) {
        if(node == nullptr) return nullptr;
        logNode(node);
        //recreate all new Nodes
        for(auto a:valToNeighbors){
            valToNewNode[a.first] = new Node(a.first);
        }
        //recrease all edges
        for(auto a:valToNeighbors){
            vector<Node*> neighbors;
            for(int i = 0 ; i < a.second.size(); i++){
                neighbors.push_back(valToNewNode[a.second[i]]);
            }
            valToNewNode[a.first]->neighbors = neighbors;
        }
        //return start
        return valToNewNode[node->val];
    }

    void logNode(Node* node){
        if(node == nullptr) return;
        //check if not visited
        if(valToNeighbors.count(node->val) != 0) return;
        //add info to adjacency list
        vector<int> neighbors;
        for(int i = 0 ;i < node->neighbors.size() ;i++){
            neighbors.push_back(node->neighbors[i]->val);
        }
        valToNeighbors[node->val] = neighbors;
        //search neighbors
        for(int i = 0 ;i < node->neighbors.size() ;i++){
            logNode(node->neighbors[i]);
        }
    }
};
```

<https://leetcode.com/problems/rotting-oranges>
Naive
- copy grid
- Start at infected, and pass down the time as it searches through the grid, incrementing by 1
- If number is higher, then adjust to be your lower value now

```cpp
class Solution {
public:
    int orangesRotting(vector<vector<int>>& grid) {
        vector<vector<int>> gridCounter(grid.size(),vector<int>(grid[0].size(),-1));
        for(int i = 0 ; i < grid.size(); i++){
            for(int j = 0 ; j<grid[0].size();j++){
                if(grid[i][j] == 1){//fresh
                    gridCounter[i][j] = INT_MAX;
                }
                if(grid[i][j] == 2){//rotten
                    gridCounter[i][j] = 0;
                }
            }
        }
        for(int i = 0 ; i < grid.size(); i++){
            for(int j = 0 ; j<grid[0].size();j++){
                if(grid[i][j] == 2){//rotten
                    search(gridCounter,0,i,j);
                }
            }
        }
        int maxTime = 0;
        for(int i = 0 ; i < grid.size(); i++){
            for(int j = 0 ; j<grid[0].size();j++){
                if(grid[i][j] == 1 || grid[i][j] == 2){ //fresh or rotten
                    maxTime = max(maxTime, gridCounter[i][j]);
                }
            }
        }
        if(maxTime == INT_MAX) return -1;
        return maxTime;
    }

    //propagate minvalues 
    void search(vector<vector<int>>& grid,int time,int x,int y){
        if(x < 0 || x >= grid.size()) return;
        if(y < 0 || y >= grid[0].size()) return;
        if(grid[x][y] == -1) return; //no orange
        if(time > grid[x][y]) return;// does not improve the time at this point
        grid[x][y] = time;
        search(grid,time+1,x+1,y);
        search(grid,time+1,x-1,y);
        search(grid,time+1,x,y+1);
        search(grid,time+1,x,y-1);
    }
};
```

<https://leetcode.com/problems/pacific-atlantic-water-flow>
Naive
- simple search

```cpp
class Solution {
public:
    vector<vector<int>> pacificAtlantic(vector<vector<int>>& heights) {
        vector<vector<int>> ans;
        if(heights.size()==0) return ans;
        int n = heights.size();
        int m = heights[0].size();
        vector<vector<bool>> pacific(n,vector<bool>(m,false));
        vector<vector<bool>> atlantic(n,vector<bool>(m,false));
        for(int i = 0 ; i < heights.size() ;i++){
            search(heights,i,0,true, INT_MIN,pacific,atlantic);
            search(heights,i,heights[0].size()-1,false, INT_MIN,pacific,atlantic);
        }
        for(int i = 0 ; i < heights[0].size() ;i++){
            search(heights,0,i,true, INT_MIN,pacific,atlantic);
            search(heights,heights.size()-1,i,false, INT_MIN,pacific,atlantic);
        }
        
        for(int i = 0 ; i < heights.size() ; i++){
            for(int j = 0 ; j < heights[0].size();j++){
                if(pacific[i][j] && atlantic[i][j])  ans.push_back({i,j});
            }
        }
        return ans;
    }

    void search(vector<vector<int>>& heights, int x, int y,bool isPacific, int prevHeight, vector<vector<bool>>& pacific, vector<vector<bool>>& atlantic){
        if(x < 0 || x >= heights.size()) return;
        if(y < 0 || y >= heights[0].size()) return;
        if(heights[x][y] < prevHeight) return;
        if(isPacific){
            if(pacific[x][y]) return; //already visited
            pacific[x][y] = true;
        }
        else{
            if(atlantic[x][y]) return; //already visited
            atlantic[x][y] = true;
        }
        search(heights,x+1,y,isPacific,heights[x][y],pacific,atlantic);
        search(heights,x-1,y,isPacific,heights[x][y],pacific,atlantic);
        search(heights,x,y+1,isPacific,heights[x][y],pacific,atlantic);
        search(heights,x,y-1,isPacific,heights[x][y],pacific,atlantic);
    }
};
```

<https://leetcode.com/problems/surrounded-regions>
Naive
- Just keep all Os that are adjacent to an edge

```cpp
class Solution {
public:
    void solve(vector<vector<char>>& board) {
        if(board.size() == 0) return;
        vector<vector<char>> cpy(board.size(),vector<char>(board[0].size(),'X'));
        for(int i  = 0 ; i < board.size() ;i++){
            if(board[i][0] == 'O') search(cpy,board,i,0);
            if(board[i][board[0].size()-1] == 'O') search(cpy,board,i,board[0].size()-1);
        }
        for(int i = 0 ; i < board[0].size() ;i++){
            if(board[0][i] == 'O') search(cpy,board,0,i);
            if(board[board.size()-1][i] == 'O') search(cpy,board,board.size()-1,i);
        }
        board = cpy;
    }

    void search(vector<vector<char>>& cpy, vector<vector<char>>& board, int x, int y){
        if(x < 0 || x >= board.size()) return;
        if(y < 0 || y >= board[0].size()) return;
        if(board[x][y] != 'O') return;
        if(cpy[x][y] == 'O') return;
        cpy[x][y] = 'O';
        search(cpy,board,x+1,y);
        search(cpy,board,x-1,y);
        search(cpy,board,x,y+1);
        search(cpy,board,x,y-1);
    }
};
```
<https://leetcode.com/problems/course-schedule>
Naive
- Cycle detection
- Go through each course, iterating through prerequisites, if we hit a duplicate throw false

Good
- Tortoise and hare pointer tactic

```cpp
class Solution {
public:
    unordered_map<int,bool> courseToIsCycle;
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {

        unordered_map<int,vector<int>> courseToPrerequisites;
        for(int i = 0 ; i < prerequisites.size() ;i++){
            courseToPrerequisites[prerequisites[i][1]].push_back(prerequisites[i][0]);
        }

        for(int i = 0 ; i < numCourses;i++){
            //cout << i << "\n";
            unordered_set<int> seen;
            bool cycle = isCycle(seen,courseToPrerequisites,i);
            if (cycle) return false;
        }
        return true;
    }

    bool isCycle(unordered_set<int>& seen, unordered_map<int,vector<int>>& prerequisites, int& course){
        if(courseToIsCycle.count(course) > 0) return courseToIsCycle[course];
        if(seen.count(course) > 0) return true;
        seen.insert(course);
        //cout << "visited: " << course << "\n";
        for(int c : prerequisites[course]){
            bool cycle = isCycle(seen,prerequisites,c);
            courseToIsCycle[c] = cycle;
            if (cycle) return true;
        }
        seen.erase(course);
        return false;
    }
};
```

<https://leetcode.com/problems/course-schedule-ii>
Naive
- Return the order you need to take to finish all courses
- 😭 its a topological sort question now
- But I could just create a adjacency list and prune it as a naive solution
- actually you know what, topological sort is trivial

```cpp
class Solution {
public:
    bool cycle = false;
    vector<int> ans;
    unordered_set<int> added;
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        unordered_map<int,vector<int>> courseToPrerequisites;
        for(int i = 0 ; i < prerequisites.size() ;i++){
            courseToPrerequisites[prerequisites[i][1]].push_back(prerequisites[i][0]);
        }
        for(int i = 0 ; i < numCourses;i++){
            //cout << i << "\n";
            unordered_set<int> seen;
            dfs(seen,courseToPrerequisites,i);
        }
        if(cycle) ans.clear();
        reverse(ans.begin(),ans.end());
        return ans;
    }

    void dfs(unordered_set<int>& seen, unordered_map<int,vector<int>>& prerequisites, int& course){
        if(added.count(course) > 0) return;
        if(seen.count(course) > 0){
            cycle = true;
            return;
        }
        seen.insert(course);
        for(int c : prerequisites[course]){
            dfs(seen,prerequisites,c);
        }
        seen.erase(course);
        ans.push_back(course);
        added.insert(course);
        return;
    }
};
```


<https://leetcode.com/problems/redundant-connection>
Naive
- Detect cycle and remove edge
- Main sharp edge is that I need to return the answer that occurs last in the input
- I have the intuition that I could just have 1 to n and as I go through edges I combine them together into the same colour and if im adding an edge that has the same colour that means that theres a cycle and the edge im adding is the last one.

```cpp
class Solution {
public:
    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        unordered_map<int,int> nodeToColor;
        for(int i = 0 ; i < edges.size();i++){
            nodeToColor[edges[i][0]] = edges[i][0];
            nodeToColor[edges[i][1]] = edges[i][1];
        }
        for(int i = 0 ; i < edges.size();i++){
            if(nodeToColor[edges[i][0]] == nodeToColor[edges[i][1]]) return edges[i];
            int a = nodeToColor[edges[i][0]];
            int b = nodeToColor[edges[i][1]];
            int m = min(a,b);
            for(auto aa : nodeToColor){
                if(aa.second == a || aa.second == b){
                    nodeToColor[aa.first] = m;
                }
            }
        }
        vector<int> ans;
        return ans;
    }
};
```

<https://leetcode.com/problems/word-ladder>
Naive
- Its a shortest path problem
