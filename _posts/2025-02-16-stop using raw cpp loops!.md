---
layout: post
tags:
  - Cpp
---
<https://www.youtube.com/watch?v=qH6sSOr-yk8&ab_channel=PauloPortela>

## **NO RAW LOOPS!**
- causes boundary access errors

If you want to grab a section of a list and move it up this list.
- Just use `rotate`!

What if you want to collect all elements of a certain property to a certain location?
- A disjoint selection!
- Just use `stable_partition`!

```cpp
int main(){
     std::vector<int> v{1,2,3,4};
     print("before ", v);

     std::rotate(v.begin(), v.begin() +1,  v.end());
     print("rotaed ", v);

     std::stable_partition(v.begin(), v.end(),  [](int n) { return n % 2 == 0;});
     print("partitioned ", v);
 }
```

Use a range library, removes a common arg!
```cpp
auto p = find(begin(a), end(a), x);
auto p = find(a, x);
```

