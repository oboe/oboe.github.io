---
layout: post
tags:
  - OS
---
<https://pages.cs.wisc.edu/~remzi/OSTEP/>
<https://github.com/remzi-arpacidusseau/ostep-code>
## Intro
Processors, fetch, decode and execute. The purpose of the OS is to make sure the hardware operates and is easy to use. We make it seem like theres an infinite amount of CPUs to run your shit, we make it seem like we have an infinite amount of memory to run your shit and instead of writing bytes directly into your disk you can use a nice file system api to interact with it.
## Processes
The key issue with sharing the CPU is that the CPU and all its registers and all it's memory can only really run one thing at once. So when we do share it we need to pull all that stuff out of there replacing it with the other process you want to run at frequent intervals to give the illusion that it's running both things. The memory side of this swapping is called paging and its done lazily.

OS maintains all process info. This includes
- Registers
- The program counter, what needs to run next
- What state is it in?
- Where the process memory is?
- It's ID?
- It's open files

## Process API
Process API has
1. `fork()`: inline control flow split of child process in same code
2. `exec()`: run a different program
3. `wait()`

## Limited Direct execution
One of the key problems OS needs to solve is how does it actually manage the CPU resource? It does this with system calls and working with hardware. The key idea is that when a program is running, it runs in user privileges and the software can invoke system calls which periodically passes the potato back to the OS to do high privilege kernel mode stuff. This is called a trap and when the computer boots the OS rushes to stuff this trap table with all the OS code places each trap should call.

The simple solution above makes sense, but what if the program knows that and never hands over control back to the OS, hogging up all the resources? Solution was to just have a timed trap calling mechanism on a timer. Which **Interrupts** your program.
## CPU scheduling
So how can we fairly schedule stuff to finish quickly? These ideas are actually opposing.
1. Round robin: super fair, but terrible turnaround time.
2. Shortest job first: super unfair, but great turnaround time.

## Multi-level feedback
Luckily smart dude Corbato figured out you can just combine all these scheduling ideas and have a bunch of parameters you can tune.
1. Have a bunch of priorities, and run those with higher priority
2. If multiple things have same priority run round robin: this is to keep things fair
3. When you have new job it starts highest priority
4. Over time each job will be demoted a priority: this is to prioritise short jobs, as short jobs will complete before they are demoted
5. Eventually we reset to reshuffle everything: this is to prevent low priority jobs from never being touched

## Lottery scheduling
Theres a bunch of other more practical ways to do scheduling.
1. Lottery scheduling is one, where each process has a number of tickets which can be randomly chosen
2. Another is stride scheduling where each process has a stride, and when a process is assigned it will take a stride, and the next process with the lowest stride is chosen
3. Finally we have the Linux Completely Fair Scheduler, which I'll talk more on below.

Linux Completely Fair Scheduler (CFS).
- Counts a number for each process as it runs.
- Every `sched_latency` time, is separated into n partitions, one for each process and the process is allocated between them at the interval times
- To avoid too many context switches, we have a `min_granularity` that specifies how small a window can be
- Finally we also want prioritisation between processes, so we can assign weights to them. `niceness`
- Additionally to avoid sleep processes hogging resources as they'll have a low stride, they are reset to the lowest stride of other processes.

## Multi-CPU scheduling
The key problem with multi CPU scheduling is that each CPU has it's own cache. This means that poor scheduling will cause each process having a lot of initial cache misses, and everything being terrible. This is the problem of **cache coherence**.

To mitigate some of the funkyness of these caches, caches can snoop on the data bus to see what other caches are doing, and if they see the data they are holding being edited, they can invalidate their cache.

**Cache affinity** is also a related concept, self explanatory, you want to run processes that run on a CPU on the same CPU so it can reuse the stuff it cached.

Linux has a bunch of multiprocessor schedulers.
1. O(1)
2. Brain Fuck Scheduler
3. Completely Fair Scheduler

## Address spaces
Now lets focus on virtualising memory. We have this large block of physical memory, how do we provide many processes access to it? We provide each program a chunk of it, this is called **address space**. 

Most basic address space looks like:
1. Program code
2. Heap
3. Stack

## Memory API
So what is the API for allocating stuff on the heap and the stack?
1. Stack: automatic allocation, with variable initialisation.
2. Heap: non automatic allocation, with malloc and new.

`malloc()`: gets you a pointer

`free()`: give it a pointer and it'll free the memory
## Address translation
You might notice that with all these virtual addresses, its nice for the user but on every memory access we are performing an address translation to get the real physical address. How do we do this well and efficiently.

Iteration 1: base and bounds relocation
- Just store a base register you add to the virtual address to get the physical address
- Also store a bounds register that you use to check if the calculated physical address is valid.

Because this is such a frequent thing to happen, theres a CPU construct called the **memory management unit** that computes this quickly.

Now theres also the sharp edge with how the OS needs to think about setting up these base and bounds for a new process. This is usually done with a free list, which lets the OS scan memory for space.

Theres two concepts I'll flag here on some problems we have right now with this basic iteration.
1. Internal segmentation: within each process memory, we have this huge space between the stack and heap that is wasted.
2. External segmentation: within our physical memory, we have a bunch of space between processes that is wasted.

## Segmentation
So lets solve this issue of internal segmentation (the chasm between the heap and stack). The idea is to have a base and bounds for each **segment**. And have these segments grow.
- This is where the term **segmentation fault** comes from, you're accessing outside the bounds of the segment!

With these segments you can do some cool stuff. Like sharing code segments between processes. Ain't that cool!

**External framentation**: when you have lots of small holes of free space across your memory after a while, making it hard to allocate more segments efficiently.
## Free space management
Lets have a step back and think about how to do this free space management efficiently.

One way is to partition this memory into fixed size portions and just scan and return the first free **page**.

An alternative is to instead have variable sizes, so you're more efficient but run into external fragmentation. You have a bunch of non useful holes now. So what are the ways to tackle this issue?
1. Compaction: when releasing memory, you should combine adjacent frees in your free list!
2. Having multiple free lists for different sizes: stops small allocations from littering large allocation space.
3. Caching: common objects are placed in these segregated free lists, faster access!
4. Binary buddy allocator: split portions into 1/2, 1/4, 1/8 partitions. Then on free you can immediately coalesce buddy portions together recursively.

Something to note is that `free()` only gets the pointer, not the size of the memory, that's because in memory theres a header portion with the size of the memory portion.
## Intro to paging
The other side to this variable allocation of segments is **paging** the act of separating space into **fixed size** pieces. The key idea is that we now view physical memory as this array of **page frames**. Now that we have programs where all there stuff is in pages, we need a way to track how to translate their virtual addresses into physical addresses. The solution is to maintain a **page table** for each process that tracks where all the pages we are using are.

The page table also encodes a bunch of other useful info
1. valid bit: indicating if virtual page is valid
2. protection bit: indicating the permissions
3. present bit: where is it, is it on disk?
4. dirty bit: has it been modified
5. ref bit: has it been accessed? Good for eviction policies.

Unsurprisingly this initial start of a page table sucks, for any virtual address we need to do another memory lookup at this page table to be able to decipher the first virtual address.
## Translation look aside buffers
The solution to this giga slow paging is to cache recently used page numbers in this hardware called the **Translation Look-aside Buffer**. This lets us skip looking at the page table. Nice!

The beauty of this solution is why contiguous memory access is fast. The VPN (virtual page number) is already cached so all subsequent reads can immediately calculate the physical address. (Some programs even configure to use super large pages, so they can always get quick reads, DBMS).

TLB is just a fully associative cache. Also has a process ID, so it can avoid serving other process addresses to the wrong processes.
## Advanced page tables
Unsurprisingly an array that maps every virtual page number to a physical page is huge. How can we make this smaller?
- One way is only tracking utilised pages, so like a free list for pages. Saves a significant amount of space!
- Another way is creating a page table tree. So have a top level page table that points to other page tables. (This slows down reads, as we need to do a second lookup, but saves space)
- We could also just store an unused page into disk, this is **swapping!**

## Swapping: mechanisms
## Swapping: policies
## Complete VM systems
## Concurrency intro
## Concurrency and threads
## Thread API
## Locks
## Locked data structures
## Condition variables
## Semaphores
## Concurrency bugs
## Event based concurrency
## Concurrency summary

