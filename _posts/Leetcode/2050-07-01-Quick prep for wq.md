Self-description C++ questions LeetCode Stock problem

Given an array of strings, sort the array based on the frequency of anagrams.

Code order book (stock glass). You have to offer data structures for the order book and implement the interface.

Implement a moving average. Trivially easy.
```cpp
Queue, maintain count

class MovingAverage {
public:
    int count;
    deque<int> dq;
    int sum = 0;
    MovingAverage(int size) {
        count = size;
    }
    
    double next(int val) {
        dq.push_back(val);
        sum += val;
        if(dq.size() > count){
            int pop = dq.front();
            dq.pop_front();
            sum -= pop;
        }
        return ((double)sum / (double)dq.size());
    }
};
```

Implement a log2(n) method, add unit tests too.


 mutable vs. immutable, memory handling in Python
```
self explanatory
- mutable updates ref value
- immutable creates a new object
```

What are you looking for when you review a merge request?

Given two arrays a and b find the intersection of these two arrays. Write code in python.

Write a SQL query to find score and Rank in a table with columns id = [1,2,3] and Score=[5,7,5] output 5:2,7:1,5:2 6.

You have 2 red, 3 green and 2 blue balls. Whats the probability you choose 2 non blue balls consecutively?

Whats the probability the sum of two die is equal to 9?

You have 60 floz of a liquid mix and you have a ratio of milk to water of 2. How much water should you add to make the ratio of water to milk equal to 2?

You have 17 shares of IBM that cost you 720 to buy. You incur a loss off five stocks. What's the real price of one IBM share?

Write a program to print the contents of a matrix in a spiral order 

Write a program to figure out the angle between an hour handle and a minute handle.

How do you find cycles in a linked list?
```
Linked list cycle detection
- Lazy, pass through with refs into a set
- floyds tortise algo. two pointers with one taking two steps
```

Write a password generator that meets these four criteria: 1- The password length is always 4 2- The password should consist letters and numbers from {A-F}, {a-f} and {1-6} and pick at least one from each of these(randomly) 3- No duplicate passwords generated 4- The password is generated totally randomly
```
Just random gen, some sort of set to check if pre generated.
```

Complexity of Bubble Sort vs Selection Sort.
```
Selection sort n^2
- 2 nested loop, select min from inner and swap that with left most val in inner loop

Bubble sort
- Start with element and bubble it up comparing adjacent up to the top
- Still n^2
```

Design a class to find the maximum number of duplicate element in two separate data file. 


Basic linux command. how to check the size of a file, how to change a file name.
```
ls -lh
mv a b
```

c++ inheritance questions
```
How does cpp handle abstractions?

With the idea of classes
- Concrete classes
- Abstract classes
- Classes in class hierachies

What is a concrete class?
- State is part of the class
- Can be allocated on stack, static mem
- Can be referenced directly, not just through refs
- You can also be resource handles to heap resources e.g vector,string

RAII
- the idea of constructor to allocate resources and destructor to deallocate resources. not rocket science.

What is a container?
- collection of elements
- new allocates memory on heap/free store
- vector a = {1,2,3}; beautiful the initialiser list constructor 😭

What are abstract types?
- decouple the interface from the representation and give up genuine local vars
- You can only allocate on heap and access through refs/pointers
- use virtual keyword to signify constructors and variables

class subclass : public superclass {
public:
	int yo;
}
How does the subclass know what function to call at runtime?
- It looks it up on it's virtual function table
```