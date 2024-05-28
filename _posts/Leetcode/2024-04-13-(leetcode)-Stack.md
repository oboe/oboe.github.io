Deque vs vector
- Vector has contiguous guarantee
- Just use a deque for queue and stack problems

<https://leetcode.com/problems/valid-parentheses>
Naive
- ?

Good
- stack, pushing and popping when possible: n time, n space


```cpp
class Solution {
public:
    bool isValid(string s) {
        deque<char> stk;
        for(int i = 0 ; i < s.size() ;i++){
            char curr = s[i];
            if (curr == '(' || curr == '[' || curr == '{') {
                stk.push_front(curr);
                continue;
            }
            char front = stk.front();
            if(s[i] == ')' && front == '(') {
                stk.pop_front();
                continue;
            }
            if(s[i] == ']' && front == '[') {
                stk.pop_front();
                continue;
            }
            if(s[i] == '}' && front == '{') {
                stk.pop_front();
                continue;
            }
            return false;
        }
        return stk.empty();
    }
};
```

<https://leetcode.com/problems/min-stack/description>
Naive
- Push, pop, top, can be supported with deque
- Hard issue is with tracking the min

Good
- I can just track the min with the each stack element: all constant, n space

```cpp
class MinStack {
public:
// each pair will be (val,current min)
    deque<pair<int,int> stack;
    MinStack() {}
    
    void push(int val) {
        if (stack.empty()) {
            stack.push_back(make_pair(val,val));
            return;
        }
        int currentMin = stack.back().second;
        currentMin = min(currentMin, val);
        stack.push_back(make_pair(val,currentMin));
    }
    
    void pop() {
        stack.pop_back();
    }
    
    int top() {
        return stack.back().first;
    }
    
    int getMin() {
        return stack.back().second;
    }
};
```

<https://leetcode.com/problems/evaluate-reverse-polish-notation/description>
Naive:
- Want a simple parseInt function

Good:
- Just a simple stack: n,n space

```cpp
class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        deque<int> intStack;
        for(string c : tokens){
            if (c == "+" || c == "-" || c == "*" || c == "/") {
                int a = intStack.back();
                intStack.pop_back();
                int b = intStack.back();
                intStack.pop_back();
                char op = c[0];
                intStack.push_back(eval(op, b, a));
            }
            else{
                intStack.push_back(stoi(c));
            }
        }
        return intStack.back();
    }

    int eval(char op, int a, int b) {
        switch (op) {
            case '+' : return (a+b);
            case '-' : return (a-b);
            case '*' : return (a*b);
            case '/' : return (a/b);
        }
        return -1;
    }
};
```

<https://leetcode.com/problems/generate-parentheses/description>
Naive:
- generate all combinations of paranetheses and check if they're valid: (2^n)*n, 2^n space

Good
- Notice theres a nice recursive relation here
- ab and (a)
- can also memoize the recursive calls

```cpp
class Solution {
public:
//(a)
//ab
    unordered_map<int,vector<string> mem;
    vector<string> generateParenthesis(int n) {
        if (mem.count(n) != 0) {
            return mem[n];
        }
        vector<string> ans;
        if (n <= 1) { //base case
            ans.push_back("()");
            return ans;
        }
        unordered_set<string> uniques;
        vector<string> smallers = generateParenthesis(n - 1);
        for(string s : smallers){
            uniques.insert("(" + s + ")");
        }
        for(int i = 1 ;i < n ; i++){
            vector<string> left = generateParenthesis(i);
            vector<string> right = generateParenthesis(n - i);
            for(string l : left){
                for(string r : right){
                    uniques.insert(l + r);
                }
            }
        }
        for(string s : uniques){
            ans.push_back(s);
        }
        mem[n] = ans;
        return ans;
    }
};
```

<https://leetcode.com/problems/daily-temperatures/description>
Naive:
- for each num, iterate forwards til you find the position: n^2, n space

Good:
- iterate back keeping stack with val and index, pop if less than: n, n space

```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        // (val, index)
        deque<pair<int,int> stack;
        vector<int> ans(temperatures.size(), 0);
        for(int i = temperatures.size() -1 ; i >= 0 ; i--){
            int curr = temperatures[i];
            if (stack.empty()) {
                stack.push_back(make_pair(curr,i));
                continue;
            }
            int back = stack.back().first;
            while(!stack.empty() && (curr >= back)){
                stack.pop_back();
                if (!stack.empty()) {
                    back = stack.back().first;
                }
            }
            if (curr < back) {
                ans[i] = stack.back().second - i;
            }
            stack.push_back(make_pair(curr,i));
            continue;
        }
        return ans;
    }
};
```

<https://leetcode.com/problems/car-fleet/description>
Naive
- nested loop, compare if car hits forward

Good
- pair pos and speed, sort, iterate through check if car hits front before target: nlogn, n space

```cpp
class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {

        // (position, speed)
        vector<pair<int,int> carInfo;
        for(int i = 0 ; i < position.size() ; i++){
            carInfo.push_back(make_pair(position[i],speed[i]));
        }
        //want low positions first
        sort(carInfo.begin(),carInfo.end());

        deque<pair<int,int> carStack;
        for(int i = 0 ;i < carInfo.size() ;i++){
            pair<int,int> currCar = carInfo[i];
            if (carStack.empty()){
                carStack.push_back(currCar);
                continue;
            }
            pair<int,int> nextCar = carStack.back();
            while(!carStack.empty() && willCollide(target, nextCar, currCar)) {
                carStack.pop_back();
                if (!carStack.empty()) {
                    nextCar = carStack.back();
                }
            }
            carStack.push_back(currCar);
        }
        return carStack.size();
    }

//naive who arrives to target first?
    bool willCollide(int target, pair<int,int> car1, pair<int,int> car2){
        int car1DistLeft = target - car1.first;
        int car2DistLeft = target - car2.first;
        float car1Hours = (float)car1DistLeft / (float)car1.second;
        float car2Hours = (float)car2DistLeft / (float)car2.second;
        return car1Hours <= car2Hours;
    }
};
```


<https://leetcode.com/problems/largest-rectangle-in-histogram/description>
Naive
- nested for loop, start and end pos of rectangle: n^2, 1 space

Good
- 10^5 meaning that nlogn solution, possible sorting is required?