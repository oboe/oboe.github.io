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
How can we wait for certain events in between threads, just spin locking seems terribly inefficient, what are the alternatives?  The solutions are **conditional variables** and **futures**!

The simplest solution is just sleeping and checking periodically with `std::this_thread::sleep_for()`.

The way you should do it is with `std::conditional_variable` which you call `wait()` and `notify_one()` on to use.

So these conditional variables, work, why do we need futures? Futures are used for **one off events**.  You can do this with `unique_future and shared_future`. One way to create a future by calling `std::async` like below.
```cpp
#include <future>
#include <iostream>
int find_the_answer_to_ltuae()
{
    return 42;
}

void do_other_stuff()
{}

int main()
{
    std::future<int> the_answer=std::async(find_the_answer_to_ltuae);
    do_other_stuff();
    std::cout<<"The answer is "<<the_answer.get()<<std::endl;
}
```

If you want to manage the execution of the async task use `std::packaged_task`!

And finally you can also use `std::promise` to have constructs to have an explicit contract between threads that means that a thread can wait on this promise until another thread fulfils the promise of some sort of data!

Huh theres a cool `std::partition` function that partitions a range depending on a condition. Thats pretty cool.
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