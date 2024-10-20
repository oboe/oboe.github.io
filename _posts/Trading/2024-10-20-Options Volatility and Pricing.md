---
layout: post
tags:
  - Trading
---

## Options land
Options: the right to buy or sell a given asset at a fixed price on or before a specific date.
Futures: must be delivered at the fixed price. Instead options gives the buyer to choose so.

Premium: options price, split into below.
- Intrinsic value, how much he makes if he exercises. Can't be less than zero.
- Time value: usually option will be worth more than just intrinsic, this is the time value.

How does the market not let people wiggle out of options contracts?
- Buyers and sellers must have clearing firms that will fulfil any obligations
- Traders will need to deposit some margin, so clearing firm and house is happy

## Basic strategies
Ignore that there is optionality to trigger the option early, what do you think the price of the underlying will be at expiration and just calculate off that.
- Main call out being that you get the options chart, where you can choose to have unlimited potential reward and fixed guaranteed downside/risk, or the reverse.

You can visualise this stuff with expiration graphs
- x axis is underlying price
- y axis is profit

## Pricing models
Traders of underlying only need to care about the direction. Options need to care about when this directional move will happen.
- This is such a pain in the ass that some ignore this directional movement and create compound options to trade on the when a directional move will happen.

Consider
- the expected return and the carrying costs
- Carrying costs is the interest you would gain if you had the money. AKA if you bought an option how much do you need to discount the final payout by?

So basically just
1. propose probabilities of all possible prices at expiration
2. Maintain an arbitrage free underlying market
3. Calculate expected return
4. From expected return deduct carrying cost

Black-Scholes model is most widely used simple option pricing model!
## Volatility
To make money as an options trader we need to care about the speed of the market as well as the direction. We care about volatility because its a measurement of this speed.

To think about price we previously:
1. thought about for every infinite price, have a probability of that, then using all those infinite price probabilities you could price your option.
2. This sucks, as it's using an infinite amount of values
3. But you can use a normal distribution to short cut it
4. With normal distributions you can easily do calculations, like finding probabilities at points and finding areas under distributions!
5. awesome!

Normal distributions also can be explained with just two numbers!
- The mean and the standard deviation

So the underlying price is the mean and volatility is standard deviation
- More specifically, volatility is one standard deviation price change, in percentage, at end of one year period.
- So 20% vol on 100, means that in a year it'll be between 80 and 120 68% of time

Theres a few issues with just using a normal distribution to model price
1. You can't really get negative cost securities, which is assumed to exist in normal distribution
2. Theres not percent based compounding, much of finance is on rate of return, and how something will grow at a fixed percentage, this is ignored if you use a normal distribution.

Whats the fix?
1. Model the percent of change with a normal distribution
2. So you're using a log normal distribution to model securities!

Estimating shorter time volatility
- Year volatility is proportional to square root of time
- So divide 20% by 16 to get the daily volatility
- This means that getting the every day settlement diffs you can guesstimate back up to yearly volatility
- e.g +1, -0.5, +1.2, +0.2, -3

Theres a few types of volatility to think about
1. Future volatility: what is the actual volatility, that you can use to determine the value of an option
2. Historical volatility: what is volatility based on past data
3. Forecast volatility: what is guess volatility in the future
4. Implied volatility: just recalc using black scholes using existing priced options on the market to figure out what other people think is the volatility. 
 
## Using the options theoretical value
What is delta?
- The rate of change in option price for every 1 change in underlying price
- So by being delta neutral you are unaffected by the price movements of a security

So you've noticed a mis-priced option, now you can
1. Purchase (sell) undervalued (overvalued) options
2. Establish a delta neutral hedge
3. Adjust hedge at regular intervals to keep being delta neutral

But it's not that easy as theres these other things you gotta consider!
1. You can freely buy and sell the contract (e.g short selling rules)
2. All traders borrow and lend at the same rate
3. Transaction costs are zero
4. There are no tax considerations

## Option values and changing market conditions
Another way to think about delta as the probability that an option will be in the money.
- An option at the money will have a delta of 0.5, aka half of the time it's worthless, so it's half as directionally sensitive than the underlying.

Cool so we have this delta thing that quantifies our directional exposure. But if my stock moves, my option delta also moves. Need something to quantify that.
1. So we have Gamma, the rate of delta change, per 1 point of price change.
2. Helps us avoid issues like the COMEX spring 1985 collapse, where people who thought they were delta neutral, quickly saw their position explode into a heavily directional position.

We also have
1. Theta: the rate at which option value decreases as time passes.
2. As expiration approaches for an at the money call, theta will skyrocket!
3. Vega/Kappa: rate at which price changes with respect to one percentage point change in volatility
4. Rho: sensitivity of option value to change in interest rates

## Spreading
One way to make money is by scalping.
- You buy at bid price and try to sell at offer price as often as possible

Another is by speculating
- You think its gonna move, and so you buy in that direction

And the one we'll focus on is spread trading
- We want to avoid market risk while im doing my nice options trading
- So we take opposing positions in different instruments at the same time.
- We expect the two instruments to have a constant price relationship
- When they start to differ, we long the underpriced and short the overpriced.
- And we hope to profit when they return

The key thing is making trades which reduce the short term risk of trades!
## Volatility spreads
137
## Risk considerations
173
## Bull and bear spreads
199
## Option arbitrage
213
## American options
241
## Hedging
257
## More volatility
273
## Stock index futures and options
301
## Inter-market spreading
331
## Position analysis
353
## Models and the real world
385