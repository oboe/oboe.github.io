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
#### The cpp memory model
**Objects** are a region of storage and in cpp everything is an object with a virtual memory location. You can touch the same object at the same time with atomic operations.
#### Atomic operations
Atomic operations are done or not done.

Cpp stores all the atomic stuff in `<atomic>`. Get them with `atomic_type or std::atomic<bool>`

`atomic_flag` needs to be initialised with `ATOMIC_FLAG_INIT`

`atomic<T>` have a bunch of atomic functions, notable ones being:
1. `compare_exchange_weak()`: can fail (return false) just because of an interrupt or something
2. `compare_exchange_strong()`: will only fail if the condition is false.
#### Synchronising operations and enforcing ordering
Same idea as distributed systems, read after write consistency ideas. You can specify memory ordering options for atomic operations to declare what ordering rules you need upheld.
1. `memory_order_relaxed`: No ordering requirement!
2. `memory_order_acquire`: when you want to do a consistent read
3. `memory_order_release`: when you want to do a consistent write
4. `memory_order_acq_rel`: when you want to do a consistent read and write
5. `memory_order_seq_cst`: (sequentially consistent) Ensure global ordering across threads! Slow af as we need to synchronise between all threads.

There exists `std::atomic_thread_fence` to create memory barriers, places where certain operations can't cross to help you do ordering.
## Designing lock based concurrent data structures
Try to keep locking to the finest granularity and to the lowest necessary type (reader, writer).

The classic reader writer lock per hash table bucket is a great example.
## Designing lock free concurrent data structures
#### Lock free meaning
A lock free data structure allows more than one thread to access the data concurrently.

A wait free data structure is a lock free structure  that doesn't have any spin loops, or retries to pause one thread.

Writing these are a pain in the ass.
#### Guidelines
1. Start with the strongest memory ordering! `memory_order_seq_cst` Then relax the constraints.
2. Use a lock free memory reclamation scheme, kinda feels like you're doing GC manually. Using hazard pointers to see if anything is access it and reference counts to see any outstanding references.
3. Be careful with ABA problem. This is an ordering issue and can be mitigated with an atomic counter to verify ordering of mutations.
4. Take note of busy wait loops!

## Designing concurrent code
#### How to divide work between threads
A key insight is that you can either have generalist or specialist threads. Do you want threads to do any work or each thread to do a specific task?

You can partition the tasks and distribute those partitions between threads.

You can assign recursive subsections to each thread.

You can partition based on task type and assign task types to each thread, running in an event loop.
#### How does performance work?
Theres a ton of considerations to how stuff actually works in the real world.
1. Number of processors and what other stuff is put on the processors.
2. Cache ping pong, memory is giga slow, don't rewrite your processor caches by jumping between threads often.
3. False sharing, processors work with cache lines and adjacent data might be in the same cache line (thread A will write to a variable close to thread Bs variable and this will tag the cache line as dirty, needing a refresh) and therefore need to be cache ping ponged between two threads.
4. Just having too many context switches between threads.

#### How to design performant data structures
The big three things to consider are
1. Contention: try to minimise the amount of data required by any thread
2. False sharing: Try to ensure data accessed by separate threads is sufficiently far apart.
3. Data proximity: Try to adjust data distribution between threads so that data thats close is worked on by the same thread. Better cache hits.

You can add `char padding[100000]` to test for false sharing.
## Advanced thread management
#### Thread pools
Have a task queue, and a pool of worker threads that poll from the task queue.
## Testing and debugging multithreaded applications
#### Types of bugs
Typically theres two categories
1. Unwanted blocking: deadlock, livelock, blocking on I/O
2. Race conditions: data races, broken invariants, lifetime issues