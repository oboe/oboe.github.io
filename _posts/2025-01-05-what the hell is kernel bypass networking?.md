---
layout: post
tags:
  - Network
  - Trading
---
## What problem is it trying to solve?
In latency sensitive workloads like HFT we're trying to shave any time possible. One common cause of latency is handing over the hot potato over and back from the OS, especially on every single network event. These are expensive because of the needless context switches and cache thrashing, sys call overheads, copying network data from NIC to kernel buffers to userspace this causes. 
## What is the solution?
A workaround to this expensive handover between user and kernel space for each network event is by just skipping the kernel and get the data directly in your application, aka: kernel bypass networking.

| API or Kit                           | NIC target | Info                                                                                                                             |
| ------------------------------------ | ---------- | -------------------------------------------------------------------------------------------------------------------------------- |
| DPDK (Data plane development kit)    | Everything | General support for all NICs. Constantly polling NIC for new packets (**Busy polling**).                                         |
| PF_RING_ZC (Zero copy)               |            | Just a technique to speed up packet capture by not shoving them into the kernel space stack                                      |
| RDMA (Remote direct memory access)   |            | More for direct server communication, not through a standard networking API like TCP. More for internal communication Id expect. |
| SolarFlare/OpenOnload                | Solarflare | Onload is general bypass functionality API, socket API                                                                           |
| TCPDirect                            | Solarflare | More latency optimised version of onload                                                                                         |
| ef_vi (efficient virtual interface)  | Solarflare | base level abstraction for solarflare                                                                                            |
| Netmap                               |            | Exposes packets, no nice API here.                                                                                               |
| eBPF/XDP                             |            |                                                                                                                                  |
| VMA (Mellanox messaging accelerator) | Mellanox   | Just OpenOnload for mellanox cards                                                                                               |

What is a DMA address?
- This is the memory area we provide to these APIs which they can write to. (Direct Memory Access)

So how can you measure and debug network perf?
- <https://docs.amd.com/r/en-US/ug1586-onload-user/sfnt-pingpong>
- <https://github.com/HewlettPackard/netperf>

## Appendix

<https://talawah.io/blog/linux-kernel-vs-dpdk-http-performance-showdown/>

<https://blog.cloudflare.com/kernel-bypass/>

<https://databento.com/microstructure/kernel-bypass>

<http://info.iet.unipi.it/~luigi/papers/20120503-netmap-atc12.pdf>

<https://lukego.github.io/blog/2013/01/04/kernel-bypass-networking/ >

<https://github.com/lukego/blog/issues/13>

<https://lwn.net/Articles/914992/>

<https://define-technology.com/hft-virtualised/>