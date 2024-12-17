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

But unsurprisingly superscalar design, processing multiple instructions at once, isn't a free lunch, theres some complexity
1. data hazards: oh no one of our instruction depend on the other: just try to merge/ forward the result directly
2. structural hazards: oh no the processor doesn't have enough capacity to handle these instructions: just have a fat register files with enough ports (an array)
3. control hazards: oh no we need to wait for conditional branches: just prefetch/ predict those branches

## Intel Pentium 4 vs Motorola G4e
79
## 64-Bit Computing and x86-64
179
## Caching and Performance
215

