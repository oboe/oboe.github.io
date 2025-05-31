---
layout: post
tags:
  - Cpp
---
## Measuring
There are four main branches of profiling
1. Instrumentation: compiler adds extra code on each function to count it
2. Debugging: profiler inserts temporary debug breakpoints at every function
3. Timer based sampling: profiler tells OS to interrupt every x time and will count where these happen, less reliable
4. Event sampling: profiler tells CPU to generate interrupts at certain events. Lets you see how many cache misses, branch mispredictions, etc happen. These are CPU specific!

RAM memory access is usually a major cause of perf issues, so we have memory caches to avoid this. These are the usually sizes. **It takes 100s of clock cycles for a RAM access but only 5 or so for a cache hit**
1. L1: 64kb
2. L2: 1MB
3. L3: 8MB

Another common concern is context switches, OS will interrupt your process to run other stuff!

Dependency chains are another concern, microprocessors will do out of order execution, so you want to avoid long dependency chains.

And a final common concern is the using the entire CPU, microprocessors can do multiple stuff to integers and floats at the same time, SIMD!
## Choosing the right algo
Before you dig into performance optimisations, first find the optimal algo!

And consider if others have already implemented already!
1. Boost
2. Intel math kernel library
3. Intel performance primitives library

## Efficiency of cpp constructs
### Variable storage
Where data is stored will affect cache efficiency.

**Stack** storage: are the fastest because the same range of memory addresses is reused again and again, so its almost certain that this part of the memory is mirrored in the L1 data cache.

**Global and static** storage: separated into three parts.
1. Constants
2. Initialised variables
3. Uninitialised variables

Main issue is that as these memory addresses arent reused, it has bad cache properties. You should just try to make all global static stuff const, as this removes a conditional check on whether if this variable is initialised or not yet.

Dynamic storage, the **heap**! Very slow, and heavily affected by heap fragmentation.

Variables declared inside a class. Main thing to note is that they have the same order of declaration so store variables that are used together in the same place!
### Integer variables and operators
Addition, subtraction, comparison, bit operations and shift operations only take 1 clock cycle!
Multiplication will take like 11, and division is like 80 🥲.
### Floating point variables and operators
Theres two different ways of doing floating point instructions.
1. Use the 8 floating point x87 register stack
2. Use vector registers XMM, YMM, ZMM

Float addition is like 5, multiplication is like 8 and division is like 40.

**JUST AVOID CONVERSIONS! between ints and floats**
### Enums
Enums are just integers.
### Booleans
Place conditional chains that are most true first in `||` for early exits!
Also bools are stored as 8 bit integers! So you can move to a char for more optimisations.
### Pointers and references
Pointers and refs are equivalent n perf and honestly the perf is not that bad for local variables. Also calling out that member pointers have a bunch of possible implementations and it youre pointing to multiple inheritance pointers then thats bad.
### Arrays
1. the best!
2. when accessing/ iterating through, you should hit adjacent bits of the array
3. if its small enough to fit in l1 cache, try to make it nice power of 2

### Branches and switch statements
Modern microprocessors do pipelined execution which they feed instructions into and get results. An issue of this pipeline is that it takes a while to figure out if something has gone wrong, like you're making the wrong cake. In reality this shows up when you feed the wrong branch of a conditional into the pipeline and you gotta redo stuff taking like 20 clock cycles.
### Functions
Something to note is that functions can slow down code by
1. causing a microprocessor jump, taking up to 4 cycles
2. code cache being less effective as you're somewhere else now
3. function parameters need to be re read
4. You need to setup the stack frame

Try to
1. Avoid unnecessary functions
2. Use inline functions
3. Avoid functions that call other functions!
4. Use macros
5. Use `__fastcall` and `__vectorcall` to speed up integer parameter functions
6. Add `static` so they are inlined, move them to anonymous namespaces!

### Function parameters
Const ref function parameters are pretty efficient, will be transferred in registers.
### Function tail calls
When last return of a function is another function, compiler will just jump to second function, not a full function call, nice! Return types need to be identical tho.
### Class data members
Just know that for your structs, data members have requirements of where the data member is placed in memory, is it on a alignment divisible by 8, 4, 2 or 1 bytes. This can leave holes in your classes!
### Runtime type identification
Guess what similar to virtual member functions, doing type identification at runtime is also slow. Who knew.
### Inheritance
Not much of a penalty with inheriting structs, but something to note is that the functions you call might be in different modules and therefore slower to call.
### Bitfields
To save space you can share memory with `union` and specify bits you're using with `bitfields`. Looks very error prone.
### Templates
Something to note is you can avoid runtime virtual functions, by pushing arguments into templates!
### Threads
Threads allow you to do multiple tasks at the same time, and these are distributed across your CPUs, at the cost of context switches every 30ms.
## Compiler optimisations
### How compilers optimise
Here's a list of things compilers will do
1. Inline functions
2. Propagate constants
3. Eliminate pointers, when target is known
4. Eliminate subexpressions that are used frequently
5. Store stuff in registers, **Main callout is that if a variable has a pointer or reference to it then it can't be stored in a register! BRUH**
6. Join identical branches, if both sides of a branch do the same thing, it will simplify
7. Remove needless conditional jumps, by copying returns earlier
8. Unroll loops
9. Move code out of loops if they're unrelated
10. Vectorisation, use vector registers for handling multiple data simultaneously
11. Algebraic reductions: **Doesn't work on floats very well!**

### Obstacles to optimisation by compiler
Theres a bunch of restrictions to compiler optimisations you should be aware of.
1. Compilers can't optimise across cpp files!
2. When accessing variables through pointers, it causes issues that the compiler can't figure out if accessed members are identical and can be reused!
3. Compilers can't know if a function is pure, so you gotta do it yourself, so it's not called a lot of times needlessly. Or try out `__attribute__((const))` on linux!
4. Virtual functions suck
5. Compilers can't do complicated algebraic reduction!

### Obstacles to optimisation by CPU
The main thing to note is to avoid long dependency chains! Avoid loop carried dependency chains!
### Optimisation directives
### Checking compiler output
Few ways to actually do this!
1. Use a compiler cli flag, `-S or /Fa`, and use a disassembler on the object file
2. If intel, use `/FAs or -fsource-asm` but will rpevent some optimisations

## Memory optimisations
### Cache code and data
### Cache organisation
Caches are organised into lines and sets. This is the n way set associative cache. So on a memory address modulo will choose which set it uses. The key thing to be aware of is how far a memory address needs to be away for it to be a cache hit or not. AKA the critical stride `num sets x line size = total cache size / number of ways
### Functions that are used together should be stored together
### Variables that are used together should be stored together
### Alignment of data
As you already know variables are auto aligned and this can cause needless holes in your structs. So you should reorder them.

You can also align large objects by the cache line size `alignas(64) int arr[1024]`. So your nice array will start at a cache line.
### Data structures and container classes
1. If the maximum number of elements is known at compile time or a decent upper limit can be set, use a fixed size array.
2. Avoid additional allocations by reserving your vectors!
3. FIFO: queue
4. LIFO: array with stack pointer
5. need ordering: sorted list, bin tree

### Explicit cache control
Modern processors already prefetch, so you `_mm_prefetch` isnt really necessary.

You can also do `__mm_stream_pi` to do writes without triggering a cache refresh.
## Multithreading
Theres three ways of doing things in parallel
1. Use multiple CPUs
2. Use multi core CPUs
3. Use out of order execution
4. Use vector operations

## Out of order execution
CPUs can actually handle more than a hundred pending operations at once, can be useful to split a loop into two and store intermediate results in order to break a long dependency chain.
## Vectorising
SIMD, single instruction multiple data operations can make stuff much faster! The vector register size depends on the instruction set you're using.

When working you can do the following to do simd with pointers better
1. `#pragma vector aligned`
2. declare functions inline

Do the following for better auto vectorisation
1. When accessing through pointers, tell the compiler explicitly that the pointers do not alias, with `__restrict or __restrict__` keyword.
2. Use less restrictive floating point operations. `-02 -fno-trapping-math -fno-math-errno -fno-signed-zeros -ffast-math`
3. 
### AVX instruction set and YMM registers
### AVX512 instruction set and ZMM registers
### Automatic vectorisation
### Using intrinsic functions
### Using vector classes
### Transforming serial code for vectorisation
### Mathematical functions for vectors
### Aligning dynamically allocated memory
### Aligning RGB video or 3 dimensional vectors
### Conclusion

## Instruction sets

## Specific optimisation topics
### Using lookup tables
### Bounds checking
### bitwise operations for checking multiple values at once
### Integer multiplication
### Integer division
### Floating point division
### Do not mix float and double
### Conversions between floats and ints
### Integer operations on floats
### Math functions
### Static vs dynamic libraries
### Position independent code
### Systems programming

## Meta programming
### Template metaprogramming
### Metaprogramming with constexpr branches
### Metaprogramming with constexpr functions

## Testing speed
### Using performance monitor counters
### Pitfalls of unit testing
### Worst case testing
## Embedded systems

## Compiler options

## Appendix
