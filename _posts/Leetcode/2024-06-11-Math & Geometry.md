---
layout: post
tags: [Leetcode]
---
<https://leetcode.com/problems/rotate-image>
Naive
- just a little edgy to implement
- kind of shambles implementing this, need to by way more clear on what i'm implementing before I code

```cpp
class Solution {
public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();
        int m = matrix[0].size();
        for(int i = 0 ; i< n/2 ;i++){
            int lim = m/2;
            if(m%2!=0) lim++;
            for(int j = 0 ; j< lim ;j++){
                int store = matrix[i][j];
                matrix[i][j] = matrix[n-1-j][0+i];
                matrix[n-1-j][0+i] = matrix[n-1-i][n-1-j];
                matrix[n-1-i][n-1-j] = matrix[0+j][n-1-i];
                matrix[0+j][n-1-i] = store;
            }
        }
    }
};
```
<https://leetcode.com/problems/spiral-matrix>
Naive
- recursively or iteratively pass through

```cpp
class Solution {
public:
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<vector<int>> visited(matrix.size(),vector<int>(matrix[0].size(),false));
        vector<int> ans;
        string lastMove = "right";
        pair<int,int> curr = {0,0};
        visited[0][0] = true;
        ans.push_back(matrix[0][0]);
        while(ans.size() < matrix.size() * matrix[0].size()){
            if(!visited[curr.first][curr.second]){
                visited[curr.first][curr.second] = true;
                ans.push_back(matrix[curr.first][curr.second]);
            }
            if(lastMove == "right"){
                if(curr.second < matrix[0].size()-1 && !visited[curr.first][curr.second+1]){
                    curr = {curr.first,curr.second+1};
                    lastMove = "right";
                    continue;
                }else {
                    lastMove = "down";
                }
            }
            if(lastMove == "down"){
                if(curr.first < matrix.size()-1 && !visited[curr.first+1][curr.second]){
                    curr = {curr.first+1,curr.second};
                    lastMove = "down";
                    continue;
                }else {
                    lastMove = "left";
                }
            }
            if(lastMove == "left"){
                if(curr.second > 0 && !visited[curr.first][curr.second-1]){
                    curr = {curr.first,curr.second-1};
                    lastMove = "left";
                    continue;
                } else {
                    lastMove = "up";
                }
            }
            if(lastMove == "up"){
                if(curr.first > 0 && !visited[curr.first-1][curr.second]){
                    curr = {curr.first-1,curr.second};
                    lastMove = "up";
                    continue;
                } else {
                    lastMove = "right";
                }
            }
        }
        return ans;
    }
};
```
<https://leetcode.com/problems/set-matrix-zeroes>

```cpp
class Solution {
public:
    void setZeroes(vector<vector<int>>& matrix) {
        bool zeroFirstIs = false;
        bool zeroFirstJs = false;
        for(int i = 0 ; i < matrix.size() ;i++){
            for(int j = 0 ; j < matrix[0].size();j++){
                if(matrix[i][j] != 0) continue;
                if(i == 0){
                    zeroFirstIs = true;
                } else {
                    matrix[i][j] = 1;
                    matrix[i][0] = 0;
                }
                if(j ==0){
                    zeroFirstJs = true;
                } else {
                    matrix[i][j] = 1;
                    matrix[0][j] = 0;
                }
            }
        }
        for(int i = 1 ; i < matrix.size() ;i++){
            for(int j = 1 ; j < matrix[0].size();j++){
                bool convert = false;
                if(matrix[i][0] == 0) convert = true;
                if(matrix[0][j] == 0) convert = true;
                if(convert) matrix[i][j] = 0;
            }
        }
        for(int j = 0 ; j < matrix[0].size();j++){
            if(zeroFirstIs) matrix[0][j] = 0;
        }
        for(int i = 0 ; i < matrix.size();i++){
            if(zeroFirstJs) matrix[i][0] = 0;
        }
    }
};
```


<https://leetcode.com/problems/happy-number>
Naive
- brute force it?

```cpp
class Solution {
public:
    bool isHappy(int n) {
        unordered_map<int,bool> seen;
        int curr = n;
        while(curr != 1){
            if(seen[curr] == true) return false;
            seen[curr] = true;
            vector<int> digits;
            string s = to_string(curr);
            for(char c : s){
                digits.push_back(c-'0');
            }
            int total = 0;
            for(int i : digits){
                total+=i*i;
            }
            curr = total;
        }
        return true;
    }
};
```

<https://leetcode.com/problems/plus-one>

```cpp
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        vector<int> ans;
        int carry = 1;
        for(int i = digits.size()-1 ; i >= 0 ;i--){
            digits[i] += carry;
            if(digits[i] == 10) {
                digits[i] = 0;
                carry = 1;
            } else {
                carry = 0;
            }
            ans.push_back(digits[i]);
        }
        if(carry == 1) ans.push_back(1);
        reverse(ans.begin(),ans.end());
        return ans;
    }
};
```
<https://leetcode.com/problems/powx-n>
```cpp
class Solution {
public:
    double myPow(double x, int n) {
        return myLongPow(x,n);
    }
    double myLongPow(double x, long n) {
        if(n==0) return 1;
        if(n==1) return x;
        if(n < 0){
            n = ~n+1;
            return 1/myLongPow(x,n);
        }
        if(n%2==0){
            double ans = myLongPow(x,n/2);
            return ans*ans;
        } else {
            double ans = myLongPow(x,n/2);
            return ans*ans*x;
        }
    }
};
```

<https://leetcode.com/problems/detect-squares>
Naive
- store points in a list
- when you get a count, go through all other points looking for a square n^3
- Because they need to be axis aligned, having something that allows fast on axis points access would be useful.
- Because its a square you can just do a simple for loop, and assume what the other two points will be, easy peasy

```cpp
class DetectSquares {
public:
    int cntPoints[1001][1001] = {};
    vector<pair<int,int>> points;
    DetectSquares() {}
    
    void add(vector<int> point) {
        cntPoints[point[0]][point[1]]++;
        points.push_back({point[0],point[1]});
    }
    
    int count(vector<int> point) {
        int x1 = point[0], y1 = point[1], ans = 0;
        for (auto& [x3, y3] : points) {
            if (abs(x1-x3) == 0 || abs(x1-x3) != abs(y1-y3))
                continue; // Skip empty square or invalid square point!
            ans += cntPoints[x1][y3] * cntPoints[x3][y1];
        }
        return ans;
    }
};
```
