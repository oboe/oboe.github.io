---
layout: post
tags:
  - Trading
---
<https://blog.headlandstech.com/2017/08/>

Companies are usually split into
1. Strategy research: programming, stats, trading intuition
2. Development: low level, networking, system architecture
3. Ops

What kind of programs exist?
1. Programs to parse exchange data, make trades, and emit orders
2. Programs that support live trading
3. Research stuff

What kind of strategies exist?
1. Arbitrage:
	1. To be competitive here, you need scale in compute
	2. Faster telco speed, microwave towers!
	3. Queue position
2. Market taking:
	1. Just help things be priced correctly, an example being recorrecting the market after a large buy order.
3. Market making
	1. Profit from bid ask spread, help connect buyers and sellers.
4. Model based:
	1. Volatility models
	2. Triangular arbitrage
	3. Implied chains
	4. Weighted constituent price calculations for ETFs
5. Rule based

Market microstructure signals: are just signals produced from data feeds.

FPGA land
- Pretty much many places just have FPGAs to do the fast execution, and have a slower controller to provide the FPGA with conditions to execute on.
- This pushes execution speed down to less than a microsecond.

