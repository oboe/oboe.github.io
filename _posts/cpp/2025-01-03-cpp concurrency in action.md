---
layout: post
tags:
  - Cpp
---
## Intro
There exists two ways of performing concurrency on modern hardware
1. Process concurrency: Processes communicate between each other, no shared memory
2. Thread concurrency: communicate through shared memory

```cpp
#include <iostream>
#include <thread>

void hello()
{
    std::cout<<"Hello Concurrent World\n";
}

int main()
{
    std::thread t(hello);
    t.join();
}
```
## Managing threads
After initialising your thread you can either
1. Wait for it with join
2. Detach it

One sharp edge of thread management is if you need the thread to finish but main path throws so you can't call join. One way of fixing this is with a RAII struct that will join on destruction.

Another sharp edge when using threads is that they don't directly support references, so you have to use `std::ref` to pass in references. It's because for thread safety it has copy parameters.

You can get a hint of the number of threads to run with `std::thread::hardware_concurrency()`. 
## Sharing data between threads
Use a mutex, easy peasy. Theres even a cool `std::lock_guard`construct that lets you use RAII to auto unlock mutexes.

`std::unique_lock()` is another fun RAII construct, with more utilities like unlocking and relocking.

Specifically for readonly constructs theres a nice `std::call_once` function that will help you guard mutex the construction of this read only thing.

cpp17 finally has a reader writer lock,  the `std::shared_mutex`, nice!
## Synchronising concurrent operations

## The cpp memory model and operations on atomic types
103
## Designing lock based concurrent data structures
148
## Designing lock free concurrent data structures
180
## Designing concurrent code
224
## Advanced thread management
273
## Testing and debugging multithreaded applications
300