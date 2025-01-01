---
layout: post
tags:
  - Cpp
---
<https://www.youtube.com/watch?v=ulOLGX3HNCI&list=WL&index=166&ab_channel=MeetingCpp>

It's a race to
1. receive market data
2. perform risk checks
3. sending the right order back

All software is in the 1-10micro s range, all hardware (FPGA, printed cad) is around 100-1000ns.

Usual characteristics of automated trading systems
1. Only few lines of code paths are important
2. Jitter is a killer
3. Very little threading/ vectorisation

The stack:
1. Network: preferring microwaves over fibre optic
2. Servers
3. Kernel tuning: need to tune BIOS, thermal headroom, tune OS, removing interrupts, process isolation
4. Cpp
5. Algos: typically public text book pricing

Main thing is that a lot of server stack is all tuned for throughput instead of latency.

On cpp general principals are
1. Move everything to compile time
2. Bypass the OS: aim for 100% userspace code, including network IO
3. Cache warm

On cpp techniques
1. Move semantics
2. Static asserts
3. Data member layout, padding alignment
4. False sharing
5. Cache locality
6. Compile time dispatch
7. Constexpr
8. Varadic templates: you can do a nice compile time recuse with varadic templates resulting in the evaluation of an overloaded base case, pretty nice <https://github.com/maciekgajewski/Fast-Log ><https://github.com/carlcook/variadicLogging/blob/master/main.cc >
9. Loop unrolling
10. Expression short circuiting: move expensive checks to the top
11. Signed, unsigned comparisons
12. Float double mixing
13. Branch prediction reduction
14. Exception
15. Slow path removal: keep fast path code together and slow code away, don't inline slow code so that it is brought into fast path code
16. Avoiding allocation: new and delete does a hot potato throw to OS
17. Fast containers
18. Lambda functions

<https://github.com/Xilinx-CNS/onload>
- you can read write packets without system calls

You have to measure to improve something
- High resolution packet in/packet out timestamping is the source of truth, with a switch