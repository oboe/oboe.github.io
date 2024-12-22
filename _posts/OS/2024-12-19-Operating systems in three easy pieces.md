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
## Multi-CPU scheduling
## Virtualisation summary
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

