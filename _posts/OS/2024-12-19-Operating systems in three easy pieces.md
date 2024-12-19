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

## Direct execution
## CPU scheduling
## Multi-level feedback
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

