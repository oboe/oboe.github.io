---
layout: post
tags: [Leetcode]
---
## Context

#### Single source shortest paths
If it's unweighted just do a BFS

If it's weighted
1. Bellman Ford: (Handles negative edges) maintain vector of distance from source, iterate over edges, n times, updating necessary distances when possible
2. Dijkstra: maintain min priority queue of edges that need processing and adjacency list. While p queue exists, pop min, process it, and add adjacent edges to the queue.
3. Floyd-Warshall: (**N cubed**, can only be used on small graphs) Maintain a distance 2d matrix, mapping node a to node b distance. Iterate through n 3 times. Updating every edge with every possible alternative node route.

#### Paths and circuits
Two kinds
1. Eulerian: goes through each edge once
2. Hamiltonian: goes through each node once: NP hard

#### Spanning trees
Whats the maximum or minimum way to connect weighted nodes/points?
1. Kruskal: goes through sorted list of edges and adds if it doesn't create a cycle. (Need to use union find structure to do this is good complexity)
2. Prims: just greedily adds min weight edge that adds anew node to the tree. (priority queue)


## Qs
<https://leetcode.com/problems/reconstruct-itinerary>
Naive
- Use all tickets once and only once
- This is the famous computer science/math bridge walking problem
- Naive solution is just start at JFK, recursively call findItinerary popping used adjacency pairs off the tickets list.
- Maybe that's fine?
- X^N? Nope when you need to go through all edges its E^2 assuming all edges are connected to all other edges
- Honestly a garbage question, need to visualise and think about a topological sort kind of intuition, who knows this shit

```cpp
class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string,vector<string>> adj;
        for(vector<string> ticket : tickets){
            adj[ticket[0]].push_back(ticket[1]);
        }
        for(auto& a : adj){
            sort(a.second.rbegin(),a.second.rend());
        }
        vector<string> ans;
        string curr = "JFK";
        int lim = tickets.size();
        dfs(curr, ans, lim, adj);
        reverse(ans.begin(),ans.end());
        return ans;
    }

    void dfs(string curr, vector<string>& ans, int lim, unordered_map<string,vector<string>>& adj){
        vector<string> adjacents = adj[curr];
        while(!adj[curr].empty()){
            string last = adj[curr].back();
            adj[curr].pop_back();
            dfs(last,ans,lim,adj);
        }
        ans.push_back(curr);
    }
};
```


<https://leetcode.com/problems/min-cost-to-connect-all-points>
Naive
- given list of points, return min cost to connect all points
- basic intuition is can find paths in n^2, and need to find spanning tree
- Fairly simple implementation, but also you need to know of prims algo :/

```cpp
class Solution {
public:
    int minCostConnectPoints(vector<vector<int>>& points) {
        vector<bool> visited(points.size(),false);
        int count = 0;
        int ans = 0;
        priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
        //choose randomly first
        count++;
        visited[0] = true;
        for(int i = 1 ; i < points.size() ;i++){
            int dist = abs(points[0][0]-points[i][0]) + abs(points[0][1]-points[i][1]);
            pq.push(make_pair(dist,i));
        }
        while(count < points.size()){
            pair<int,int> minEdge = pq.top();
            pq.pop();
            if(visited[minEdge.second]) continue; // already visited
            visited[minEdge.second] = true;
            ans += minEdge.first;
            count++;
            for(int i = 1 ; i < points.size() ;i++){
                int dist = abs(points[minEdge.second][0]-points[i][0]) + abs(points[minEdge.second][1]-points[i][1]);
                pq.push(make_pair(dist,i));
            }
        }
        return ans;
    }
};
```

<https://leetcode.com/problems/network-delay-time>
Naive
- Single source, find min distance for all nodes to receive the signal, so it's get the max shortest path to each node!
- No negative edges so we can use Dijkstras!

```cpp
class Solution {
public:
    int networkDelayTime(vector<vector<int>>& times, int n, int k) {
        vector<bool> visited(n+1,false);
        vector<int> distance(n+1,INT_MAX);
        priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>> pq;
        distance[k]=0;
        pq.push(make_pair(0,k));
        while(!pq.empty()){
            pair<int,int> minEdge = pq.top();
            pq.pop();
            if(visited[minEdge.second]) continue; // already visited
            visited[minEdge.second] = true;
            for(vector<int> time : times){
                if(time[0] != minEdge.second) continue;
                if(distance[minEdge.second]+time[2] < distance[time[1]]){
                    distance[time[1]] = distance[minEdge.second]+time[2];
                    pq.push(make_pair(distance[time[1]],time[1]));
                }
            }
        }
        for(int i=1;i<=n;i++){
            if(!visited[i]) return -1;
        }
        int ans = 0;
        for(int i = 1 ;i < distance.size() ;i++){
            ans = max(ans, distance[i]);
        }
        if(ans == INT_MAX) return -1;
        return ans;
    }
};
```

<https://leetcode.com/problems/swim-in-rising-water>
Naive
- whats the highest water where start and end are connected
- Perform Dijkstras but instead of a distance, maintain a max height map!

```cpp
// Cpp17 structured bindings are beautiful!
std::tuple<int, int, int> triple = std::make_tuple(1, 2, 3);
auto [first, second, third] = triple;
```

```cpp
class Solution {
public:
    int swimInWater(vector<vector<int>>& grid) {
        vector<vector<bool>> visited(grid.size(),vector<bool>(grid[0].size()));
        vector<vector<int>> height(grid.size(),vector<int>(grid[0].size(),INT_MAX));
        priority_queue<tuple<int,int,int>,vector<tuple<int,int,int>>,greater<tuple<int,int,int>>> pq;
        height[0][0]=grid[0][0];
        pq.push(make_tuple(height[0][0],0,0));
        while(!pq.empty()){
            auto [pqDist, pqX, pqY] = pq.top();
            pq.pop();
            if(visited[pqX][pqY]) continue; // already visited
            visited[pqX][pqY] = true;
            vector<pair<int,int>> adj;
            if(pqX > 0) adj.push_back({pqX-1,pqY});
            if(pqY > 0) adj.push_back({pqX,pqY-1});
            if(pqX < grid.size()-1) adj.push_back({pqX+1,pqY});
            if(pqY < grid[0].size()-1) adj.push_back({pqX,pqY+1});
            for(pair<int,int> a : adj){
                if(max(height[pqX][pqY],grid[a.first][a.second]) < height[a.first][a.second]){
                    height[a.first][a.second] = max(height[pqX][pqY],grid[a.first][a.second]);
                    pq.push(make_tuple(height[a.first][a.second],a.first,a.second));
                }
            }
        }
        for(vector<int> vv : height){
            for(int ii : vv){
                cout << ii << " ";
            }
            cout << "\n";
        }
        int ans = height[grid.size()-1][grid[0].size()-1];
        if(ans == INT_MAX) return -1;
        return ans;
    }
};
```

<https://leetcode.com/problems/cheapest-flights-within-k-stops>
Naive
- min path from source to destination
- the sharp edge is the at most k stops restriction
- does it contain negative edges? does it contain negative cycles?
- How do I maintain the number of stops while I finding out the cheapest path
- do I need to just maintain another node to stops, and refuse updating dst if it doesn't have enough stops?
- Ohh it's at most k stops, so 

Good
- Build adjacency list for fast access
- BFS, layer by layer processing, for loop within, give up after k
- maintain nodeToCost mapping, continue to update it when processing an edge