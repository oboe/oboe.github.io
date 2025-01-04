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

## L3 Internet Protocol (IP)
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
One problem internet had was a lot of cyber attacks, to mitigate this we have: **Firewalls** are just routers that restricts what type of traffic it forwards.

Another problem is that IPv4 addresses are running out and they're getting quite expensive, to mitigate this we have: **NAT network address translation** gateways, they're just things which allow duplicate addresses to be used within a gated network.
#### Firewalls
Two types:
1. Proxy firewalls: Application layer gateway, terminating connections and creating internal only connections. SOCKS, HTTP proxy are examples.
2. Packet filtering firewalls: drops IP datagrams, acts as a router. Use filters and ACLs to control.

#### Network Address Translation
NAT needs to consume all ingoing and outgoing datagrams so it can rewrite the addresses and fix checksums.

For TCP, theres the **three way handshake of SYN, SYN-ACK, ACK,** on NATs on first SYN we'll forward it to a random internal IP and add this to our mapping table, if we do't get a SYN-ACK back we can remove the entry as a connection wasn't established. Or when we receive a FIN we can clear it up.

Instead for UDP that doesn't have a handshake or closing, we can just have a time based eviction policy to clean up our table.
#### NAT Traversal
Theres a bunch of cool strategies that exist with NAT
- Hairpinning/ NAT loopback: on a private to private connection just do no additional work and just continue to map private to private
- Pinhole/ Hole punching: establish a private to public connection, and then with the new info, establish a public to public connection directly. Skype does this! STUN protocol helps with this.
- TURN (traversal using relays around NAT): just give up going through NAT and just go through a third party server.
- ICE (Interactive Connectivity Establishment): P2P, establish connections

## Broadcasting and Local Multicasting (ICMP and MLD)
#### Intro
There are 4 kinds of IP addresses
1. Unicast
2. Anycast
3. Multicast
4. Broadcast (No IPv6)

The key purpose of multicast and broadcast is to deliver packets to multiple places and to discover servers or clients.

How does L2 link layers efficiently to multicast and broadcast?

The main difference between multicast and broadcast is that, multicast only involves those that support a specific service or protocol.

Usually only UDP does multicasting. TPC is for connections.
#### Broadcasting
Routers simply forward data to all receivers. The all 1 bit address is the broadcast address (or just the last address in a subnet).
#### Multicasting
Instead of sending data to all people, lets just send data to anyone who is interested in it. Hosts and routers maintain state on if they're interested.
1. People join a group, sending IGMP message to a router
2. When router gets a multicast address (224.0.0.0 > 239.255.255.255 or 00:00:5e address)
3. It will blast it to any subscribed people

Use `netstat -rn` to view your routing table.
## User Datagram Protocol (UDP) and IP Fragmentation
#### Intro
UDP provides, datagram oriented, L4 transport layer protocol, preserving message boundaries and checksums. Does not provide, error correction, sequencing, duplicate elimination, flow or congestion control.

The UDP datagram look like, UDP stuff and header is stuffed into the data slot.
1. IPv4 header
2. UDP header
	1. Source port number
	2. Destination port number
	3. Length
	4. Checksum
3. UDP data

#### UDP checksum
The checksum is computed over the UDP data and UDP header, and some of the IPv4 header. This is why NAT gateways need to edit at the L3 IP layer but also the L4 transport layer as well, so it can update this checksum. 
#### UDP and IPv6
There exists a teredo project to tunnel IPv6 on IPv4, because of the lack of quick support of IPv6.
#### IP fragmentation
When package is too big IP protocol will fragment it into smaller pieces. IPv4 this can happen at source or any intermediate routers, IPv6 this happens only at source. A major issue of this, with UDP is that datagrams can be lost and you can't reassemble them at all then! 
#### Path MTU Discovery with UDP
Use Internet Control Messaging Protocol, ICMP, thats just a message a router will send back to you to tell u stuff like your package is too big or I can't get to the destination.
#### UDP server design
Something to note is that the server is primitively handed the UDP data block, the IP and UDP headers are stripped often. So if you need them you'll need to keep that in mind.
#### UDP in the internet
UDP looks to account for 10 - 40% of internet traffic. And looks like much of use is in media playing and tunneling use cases.
## Name resolution and Domain Name System (DNS)
#### Intro
Remembering IP addresses sounds awful, so we have a big hierarchical database that maps host names to IP addresses.
#### DNS name space
DNS names are organised in a namespace. Top level domains, subdomains and URL labels.
#### Name servers and zones
So what if you're managing a portion of name space? You need some **name servers**, for your "zone". And will have delegation records to handover smaller subtree zones to other name servers.
#### Caching
Most name servers, outside of some root TLD servers will cache zone info as they learn, with a TTL eviction policy. Each DNS record, name to IP address mapping has a TTL.
#### DNS protocol
Two sides to the protocol
1. Hitting the DNS: standard requests
2. Controlling DNS: zone transfers, DNS notify.

| Resource Record | What is it?                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| A, AAAA         | Address Record, map a name to a IP                                                                            |
| NS              | Name server, what are the authoritative name servers for a domain                                             |
| CNAME           | Canonical Name records, these are aliases to point to other resource records!                                 |
| SOA             | Authority Records, Start of Authority, point to other name servers which are the authority of certain domains |
| PTR             | Reverse DNS lookup queries, Pointer queries. Lets you do a reverse lookup.                                    |
| MX              | Mail exchanger records: not super widely used now                                                             |
| TXT             | any text, such as anti spam for email, or verifying ownership                                                 |
| SRV             | Service Records, like a general MX, you can specify what kind of protocol, ports a service supports           |
| NAPTR           | Name authority pointer records, more complex mappings                                                         |
| OPT             | Allows extra features                                                                                         |

Query DNS with `dig`
## Transmission Control Protocol (TCP) basics
#### Intro
IP and UDP do no error correction.

Theres four categories of communication failures
1. Packet bit errors: fixed with error correcting codes
2. Packet reordering: fixed with sequence numbers
3. Packet duplication: fixed with sequence numbers
4. Packet erasure: retry based on an estimate of round trip time

#### Intro to TCP
UDP provides a package sending interface, TCP instead provides a **connection oriented** interface, you send and get byte streams.
- TCP breaks up this byte stream into packets
- Numbers these packets
- Wraps these packets (segments) in IP datagrams
- And repackages these at the other side back into a byte stream
- TCP waits for acknowledgement of packets, and if it doesn't get it it'll retransmit the packages.

#### TCP header and encapsulation
Unsurprisingly TCP has a header that wraps its TCP data in each IP datagram.

| Header                 | What is it?                                                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------- |
| Source port            | just a port                                                                                           |
| Destination port       | just a port or "socket"                                                                               |
| Sequence number        | What number segment is this in the stream                                                             |
| Acknowledgement Number | Number the sender expects to receive next                                                             |
| Header Length          |                                                                                                       |
| Resv                   |                                                                                                       |
| CWR                    | Theres a bunch of bit fields defined in TCP. This is the congestion window reduced: slow down pls bit |
| ECE                    | Echo: sender received an earlier congestion notification                                              |
| URG                    | Urgent: urgent pointer field is valid                                                                 |
| ACK                    | on when a connection is established                                                                   |
| PSH                    | receiver should push this data asap                                                                   |
| RST                    | reset the connection                                                                                  |
| SYN                    | synchronise sequence numbers to initiate a connection                                                 |
| FIN                    | Ive finished sending all my data                                                                      |
| Window Size            | This is the sliding window thats filled as we send back ACKs                                          |
| TCP checksum           | Similar to UDP, spans TCP header, data and some IP headers                                            |
| Urgent Pointer         | not used much                                                                                         |
| Options                | 🤔                                                                                                    |

## TCP connection management
#### Intro
UDP is connectionless protocol.

TCP is a connection protocol. TCP will detect and repair all data transfer problems, like packet loss, duplication and errors.
#### TCP connection establishment and termination
TCP connection is between a pair of IP and port.

TCP has three phases
1. Setup a connection
	1. Client sends a SYN segment with port it wants to connect to and clients initial sequence number
	2. Server sends SYN segment and its own sequence number. AND it ACKs the clients message, by returning clients ISN + 1.
	3. Client ACKs the servers segment, by returning servers ISN + 1.
2. Transfer of data
3. Closing a connection
	1. Client sends a FIN segment.
	2. Server ACKs the clients FIN segment by returning clients ISN + 1.
	3. Server sends a FIN.
	4. Client ACKs the FIN.

When TCP gets a segment there are two things it requires
1. Valid checksum
2. But also a ISN (sequence number) that is within its sliding window

**ARP**: address resolution protocol maps IP addresses to MAC addresses. It's a L2 link layer protocol. Works by broadcasting "who has the MAC for this IP", getting a response, and done.
#### TCP options
TCP has a bunch of options, here's some
1. Max Segment Size: yup its written on the tin
2. Selective Acknowledgement: by default you need to receive segments sequentially so when you have holes its a problem, you can send a SACK segment to indicate 3 holes you want to patch.
3. Window Scale: Lets us increase our sliding window
4. Timestamp options: lets you add some telemetry info of timestamps to get the round trip time. And avoid crappy issues with sequence numbers wrapping around.
5. User timeout: lets you tell the other guy your timeouts.
6. Auth: lets you authenticate TCP segments with hashes.

#### TCP server operation
How does a TCP server usually operate?

Usual is TCP connection request arrives at a server, server accepts connection and hands over the connection to a new process or thread to handle the client.

Usually berkeley socket API is used and this has queues per endpoint of connections that are about to be established. Main call out is that application API already has the three way handshake abstracted over already.
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
