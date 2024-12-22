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
## Memory API
## Address translation
## Segmentation
## Free space management
## Intro to paging
## Translation look aside buffers
## Advanced page tables
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

