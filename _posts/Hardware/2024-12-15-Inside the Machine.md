---
layout: post
tags:
  - Hardware
---
## Basic computing concepts
Key structure in the toy computer is
1. Storage: has both the instructions and free space
2. Registers: ultra fast data access on cpu
3. Arithmetic logic units
4. data buses

Key call out is that each instruction can only be a
1. Arithmetic instruction
2. Memory access instruction: loading and storing from main memory (including branch jump instructions here as well)

## Mechanics of program execution
Fun call out is that when you turn on a computer, you're starting the bootstrapping. But how does the computer start doing anything without any instructions?
1. If first looks up BIOS: readonly program to setup all the hardware stuff
2. Then BIOS hands over to bootloader program that goes and finds the OS
3. Then the OS program sets up all your own programs

## Pipelined execution
Modern RISC style processors have four steps
1. Fetch
2. Decode
3. Execute
4. Write

The CPU has a speed at which it can execute all these four steps. If it waits for an full loop, that means that while we're fetching we aren't executing or writing and while we're writing we arent fetching. We have cool hardware just sitting around. To fix this issue most modern processors are pipelines so a line of instructions are processed as a pipeline in the processor.
## Superscalar execution
To make computers even faster we realised we could just shove two logic units together, this is the idea behind superscalar computers, they can process multiple scalars (numbers) at once. Nothing complicated.

Unsurprisingly hardware has specialised to process fundamental data easier.
- Scalar ints
- vector ints
- scalar floats
- vector floats

How might the stack look?
1. Your program talks to
2. Instruction set architecture (ISA)
3. converted to talk to
4. Any same architecture hardware

In these ISA, Intel added new cool stuff to do faster processing.
1. MMX (multimedia extensions)
2. SSE, SSE2 (streaming SIMD extensions)
3. SIMD = Single Instruction Multiple Data

But unsurprisingly superscalar design, processing multiple instructions at once, isn't a free lunch, theres some complexity
1. data hazards: oh no one of our instruction depend on the other: just try to merge/ forward the result directly
2. structural hazards: oh no the processor doesn't have enough capacity to handle these instructions: just have a fat register files with enough ports (an array)
3. control hazards: oh no we need to wait for conditional branches: just prefetch/ predict those branches

It's shocking that vectorised perf is equivalent to scalar instructions on modern processors.
## Intel Pentium 4 vs Motorola G4e
The key design differences are
- Intel pushing for clock speed and deeper pipelines, leads to higher risk of bubbles clogging up the pipeline
- G4e pushing with more parallel functional units, which needed a submission queue to be well used

Something that is talked about a lot is the pain of branch prediction and how necessary it is. It's so expensive to just wait for many cycles waiting to get something from non L1 cache, so lot of work is put into predicting. Such as compiler hints and Intels trace cache, just speculatively inlining branch instructions out.
## 64-Bit Computing and x86-64
Intel wasn't good enough so AMD beat them with creating a more popular Instruction Set Architecture called x86-64.
## Caching and Performance

| Level       | Time    | Size  | Tech     | Managed By |
| ----------- | ------- | ----- | -------- | ---------- |
| Register    | 1ns     | 1kb   | CMOS     | Compiler   |
| L1          | 2ns     | 10kb  | SRAM     | Hardware   |
| L2          | 5ns     | 5MB   | SRAM     | Hardware   |
| Main Memory | 30ns    | 1GB   | DRAM     | OS         |
| Hard Disk   | 3mil ns | 100GB | Magnetic | OS         |

The key principle behind cache locality working is
1. Spatial locality: stuff you just accessed neighbours are likely needed next
2. Temporal locality: stuff you just accessed is likely to be reaccessed soon

Cache usually simplified into blocks, and usual caching strategies exist, fully associative, n-way associative, direct mapping styles. Can't do cool eviction policies as it's too expensive, it gotta be cheap if it's done so often.