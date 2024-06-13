<https://www.youtube.com/watch?v=BxfT9fiUsZ4&list=WL&index=2&ab_channel=Pacific%2B%2B>

Need to think about hotpath/fastpath that is only exercised 0.01% of the time that executes the trade. Any jitter is unacceptable. OS, network, hardware are all forgotten about this code, they all work in fair ways which ignore this code. 

Wire to wire time is seeing order from exchange to making your order. Usually you have 1 microsecond to do all your compute. Thats about 3k CPU cycles. Game over if you go to main memory.

Can view a compiled code with this site
- <https://godbolt.org/>

Easily benchmark code with google benchmark
- <https://github.com/google/benchmark>

You need to tune the hardware to even get to a level playing field. e.g removing hyperthreading to avoid your cache getting messed up.

Push away any unnecessary handling outside of the hotpath!

Template based configs
- It's convenient to have things controlled via config files, but virtual functions can be expensive.
- Use templates to avoid this. Removes branches and eliminates code that won't be executed.

Memory allocation
- It's expensive, don't use new or delete in the hotpath

Don't use if statements
- Reduce branch mispredictions

Try to avoid multithreading when you can
- Avoid contention between threads, locks are expensive

Just denormalise data to avoid lookups

unordered map
- typically backed by a single linked list
- buckets are pointers to different parts of the linked list
- There should be 1 item per bucket
- When theres more than that then you need to rehash, becomes super slow
- so as it's a linkedlist its going to be cache inefficient
- consider using googles dense_hash_map! Which uses contiguous memory
- optiver did a combination of both.

Branch prediction hints
- Add macro to give compiler a hint on what branch to prioritise
- Actually doesn't help in HFT, the branch predictor is the main issue. Try to avoid branches!

inline
- Always inline, non inline, be careful
- Be careful to avoid inlining unnecessary code.
- Can also give other gcc compiler hints like hot and cold to put functions into same of different sections.

prefetching
- `__builtin_prefetch` Can be useful, if you know hardware branch predictor wont be able to work out the right pattern

keep the caches hot
- Lie on the system, just tread through the whole hot path code, to continually keep the cache hot

Hardware consideration
- server has N cpus
- each cpus have N cores
- each core has L1 data cache, L1 instruction cache, L2 cache 512kb
- all cores share a unified L3 cache, which is huge mb
- Just disable all but 1 cpu

just avoid strings and allocations
- use something like in place string so the allocation is all on the stack

Be careful of enums and switches

Be careful of std pow, can be super slow
