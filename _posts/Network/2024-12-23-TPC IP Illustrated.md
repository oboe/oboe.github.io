---
layout: post
tags:
  - Network
---
## Intro
Lets do a whirlwind tour of the entire stack and what it looks like.

One of the key principles is **multiplexing**: which just means that instead of having a connection using a cable for a period of time, you chunk communication into packets so you can share this cable between multiple people.

This packet idea was further developed with the addition of source and destination metadata to each of these packets: **datagrams**. This is great because now all the switches and routers in between the computers don't need to have any state management, they are just dumb pipes forwarding datagrams.

The idea of **fate sharing** also follows where all the necessary state needed to maintain an active communication must be at the source and destination endpoints.

Another principle is this idea of implementing the right features at the right level/abstraction. And not making immature abstractions at too low of a level. With this principle the layering idea of network protocols emerge. This is super neat. The real neat thing here is that each layer will blindly encapsulate the data it gets, wrapping it in its own metadata header and computers will only unwrap these packets as necessary upwards.

OSI model
1. Physical: **How to actually sent bits across a cable**. connector, data rate, encoding info, low level error correction. Ethernet 1000BASE-T
2. Link: **How to communicate across a single link**. error detection. Ethernet, Wi-Fi.
3. Network: **How to communicate across multiple hops**. IP datagram, let us hop across different links.
- From here the stuff is only implemented on client/servers.
1. Transport: How to communicate across multiple programs running on same computer system, and possibly reliable delivery. TCP.
2. Session: How to establish and create an ongoing connection. ISO X.225
3. Presentation: How to communicate data formats, like ASCII.
4. Application: Whatever you want to do.

Theres three main components to network
1. Computers: these are the end things that communicate
2. Switches: these operate at link layer, and forward packets as necessary to the right MAC-id device within network.
3. Routers: these connect networks, operating at network later, forwarding packets to the right IP address.

## L3 Internet address architecture
Lets have a look at IP addresses the L3 Network layer addresses.
1. Every device connected to the internet has one
2. DNS maps URLs to them
3. They are allocated to users and orgs, usually users just rent internet service provider addresses.

How do they look
- IPv4: look like `255.255.255.255`
- IPv6: look like `y:y:y:y:y:y:y:y`

Network address translation (**NAT**): self explanatory but these rewrite IP addresses in datagrams as they enter the internet.

Classless Inter-Domain Routing (**CIDR**): is just moving away from the fixed A,B,C class system of addresses and now you just signify a group of addresses with a int prefix signifying the number of bits needed for the network.

You can view network interfaces with the `ifconfig` command.

You can view domain, IP, registrar info with the `whois` command.
## L2 Link layer
The purpose of the link layer is to send and receive IP datagrams. Simple!
- Theres a bunch of these
- They transfer protocol data units **PDUs** or frames, that are less than a kb

#### Ethernet
Sends Ethernet frames these have
1. Preamble: for decoding the payload tells us space between encoded bits so we can read it
2. Start Frame Delimiter SFD
3. Destination DST (MAC address)
4. Source SRC (MAC address)
5. Type: what type of data follows, IPv4, IPv6, ARP
6. Some tags
7. Payload
8. CRC: integrity check

You also need to wait 12 byte worth of time before sending your next eth packet,
#### Full duplex, power save, auto negotiation
Half duplex just means you can send stuff down the cable in one way at a time, full duplex means you can send both ways at a time 

#### Bridges and switches
Bridges and switches connect physical link layer networks. But how does a switch know where to send stuff to the right MAC address? It maintains a mini table and populates it slowly as it receives new frames! This table has time based eviction policy.

#### WiFi (IEEE 802.11)
WiFi frames are fairly similar to ethernet frames. One key difference is the addition of a **frame control word** to specify the type of frame this is, these can be:
1. Management Frames: how wifi access points communicate fundamental metadata and establish connections
2. Control Frames: For control flow and acknowledgement of frames. WiFi is less reliable than cable so we resend packets if we don't get an ACK.
3. Data Frames: Pretty self explanatory, but you can also combine and separate frames into more easily transmittable chunks.

## Internet Protocol (IP)
#### Intro
IP datagrams deliver all the TCP, UDP, ICMP, IGMP data. 
- It's all best effort does not give a shit to redeliver or handle failures.
- It maintain no connection state.
- It can duplicate or fail to deliver its datagrams, it does not care lmao.

#### IPv4, IPv6 headers
It's 20 bytes contains all the expected metadata like version, checksum, TTL, source and destination etc.

| Header (IPv4)                           | What is it?                                                                                                                                                           |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Version                                 | Main call out is that version field is identical, but everything else is different in IPv4 and IPv6, a host handling both is where the name **dual stack** come from. |
| IHL (Internet Header Length)            | Just the number of 32 bit words are in the header                                                                                                                     |
| DSField (Differentiated Services Field) | To help with network congestion, set by routers. How much priority should I get?                                                                                      |
| ECN (Explicit Congestion Notification)  | To help with network congestion as well, set by routers.                                                                                                              |
| Total Length                            | Total length of the IPv4 datagram, 16 bits so max IPv4 datagram size is 65k bytes                                                                                     |
| Id                                      | Unique field, don't mix up fragmented datagrams                                                                                                                       |
| Flags                                   | 🤔<br>                                                                                                                                                                |
| Fragment Offset                         | 🤔<br>                                                                                                                                                                |
| Time to live                            | Actually a hop limit, no one actually asserts on the time                                                                                                             |
| Protocol                                | Whats the protocol type of data are we carrying?                                                                                                                      |
| Header checksum                         | Self explanatory (Not CRC, it's a more simple internet checksum)                                                                                                      |
| Source IP address                       | 32 bit IP addresses                                                                                                                                                   |
| Destination IP address                  | 32 bit IP address                                                                                                                                                     |
| Options                                 | All proposed IPv4 options are basically not used. IPv6 has a bunch more useful ones: like Jumbo payload, padding, tunnel limits, etc.                                 |
| IP data                                 | The meat and potatoes!                                                                                                                                                |

**MTU, maximum transmission unit**: self explanatory, whats the max packet which can be sent over a network without needing to break it down.
#### IPv6 extension headers
IPv6 has a bunch of additions to the IPv4 heading structure.

| Header (IPv6)   | What is it?                                                                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Routing Header  | You can specify nodes you want your datagram to visit before it reaches its end goal. Works by overwriting the destination IP address as you visit o journey nodes. |
| Fragment Header | Just IPv4 with a larger identification bit.                                                                                                                         |

#### IP forwarding
General ordering of handling all this IP stuff is
1. I get an IP datagram, from another protocol or network interface
2. I check if I'm the destination IP
3. I open up my routing table, to find the corresponding IP
4. I crack open the header for the protocol or next header field
5. I blast the datagram to the next routing node, with that protocol
6. If I can't find it in my routing table, I either discard or send it back?

So what does this routing table look like?
1. Destination
2. Mask: 32 bit (IPv4) to scope down the destination to compare with where you need to go
3. Next hop: contains IP address of next IP entity you need to send to
4. Interface: What is the network interface I actually need to send stuff into to for this destination

How does it work? We just pick the matching masked destination with the most bits.

View hops with `> traceroute -n google.com`

## Firewalls and Network Address Translation (NAT)
#### Intro

#### Firewalls

#### Network Address Translation

#### NAT Traversal
## Broadcasting and Local Multicasting (ICMP and MLD)
#### Intro

#### Broadcasting

#### Multicasting

## User Datagram Protocol (UDP) and IP Fragmentation
#### Intro
#### UDP header

#### UDP checksum
#### Examples

#### UDP and IPv6

#### UDP Lite
#### IP fragmentation
#### Path MTU Discovery with UDP

#### Interaction between IP fragmentation and ARP/ND
#### Maximum UDP datagram size

#### UDP server design

#### Translating UDP/IPv4 and UDP/IPv6 datagrams

#### UDP in the internet

## Name resolution and Domain Name System (DNS)
#### Intro
#### DNS name space
#### Name servers and zones

#### Caching
#### DNS protocol
## Transmission Control Protocol (TCP) basics
#### Intro

#### Intro to TCP

#### TCP header and encapsulation
#### Summary

## TCP connection management
#### Intro
#### TCP connection establishment and termination
#### TCP options
#### Path MTU discovery with TCP

#### TCP state transitions
#### Reset segments
#### TCP server operation

## TCP timeout and retransmission
#### Intro
#### Simple timeout and retransmission example

#### Setting the retransmission timeout

#### Timer based retransmission
#### Fast retransmit

#### Retransmission with selective acknowledgements

#### Spurious timeouts and retransmissions

## TCP data flow and window management
#### Intro

#### Interactive communication

#### Delayed acknowledgements

#### Nagle algorithm

#### Flow control and window management

## TCP congestion control
#### Intro

#### Standard algorithms

## TCP keep alive
#### Intro
#### Description
