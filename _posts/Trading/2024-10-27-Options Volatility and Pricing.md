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
You're keeping delta neutral but you want to make market bets. There's four main categories of ways you can place a group of orders you can do here.
1. Backspread (or ratio spread): You have more long than short options, all expiring at same time. Gives us profit if price moves in either direction, and has uncapped gain in a single direction.
2. Ratio vertical spread: opposite of backspread. You're betting that stock keeps constant. With a single direction uncapped downside.
3. Straddle: the classic both direction uncapped upside or downside. (Or if made at different prices, it's a strangle)
4. Butterfly: capped upside or downside
5. long time spread (Or calendar spreads): Opposing positions which expire in different months. Profit when market sits still. Exploiting that short term expiration will decay faster than long term expiration. But also caveat that if volatility increases, options can increase in value and that might outweigh the options getting hit by the market moving in a direction. 
6. short time spread: Profit when market moves. Opposite of long time spread.

Key call out is that backspreads, ratio vertical spreads, straddles, etc all want real vol and implied vol to both rise of fall. Time spreads want the two to differ.
## Risk considerations
You can think about each of the greeks as a form of risk you want to take.
- Delta (Directional) Risk: risk of movement in one direction
- Gamma (Curvature) Risk: risk of movement in either direction
- Theta (Time Decay) Risk: risk of no movement
- Vega (Volatility) Risk: risk of us using wrong volatility
- Rho (Interest Rate) Risk: risk of interest rate changing
- Liquidity Risk: risk of not being able to exit or adjusting positions

A key ball part estimate thing you can do to compare spreads is dividing your risk values, your greeks by theoretical edge to get a number for the amount of risk you're taking for each point of payoff.

Delta adjustment
- Over time your trades change in exposure, such as delta (your market direction).
- You can adjust this without affecting your other risks by just buying the underlying contract. Of course buying options of your underlying contract will change your risks.

## Option arbitrage
Using options you can recreate other positions. These are called synthetic positions.

For example, long a June 100 call and short a June 100 put, is just a synthetic long position.
- This relationship between call, put and underlying means that you can calculate the expected price of one from the other two.
- This is called put-call parity

Arbitrage, is when you sell on one market, and buy on another. To have a delta neutral position to make a profit on the difference between the two markets.

Difference between stock vs futures type settlement: when you exercise a stock type, you get the actual stock in your account, when you exercise a futures type you get cash in your account.

You can look for these mispricings. And notice anything weird. Like, is put call parity maintained? Is the thing with more expiration time costing more?
1. Are there any basic conversions and reversals?
2. On vertical spreads and butterflies
3. On straddles and time spreads

You don't need a glass ball to predict some price, you can just try to make money off fixing this inconsistencies.
## American options
European options can only be exercised at expiration, American options can be exercised whenever.

When should you want to exercise an American option before expiration?
- In future type settlement markets: theres no reason to exercise an option. You are better off holding it or selling it. Theres no interest benefit in exercising an option.
- For stock type settlement: you can consider exercising an option to avoid losing out on some dividends for calls. For puts you can consider exercising whenever the interest to be gained looks good.

The basic black scholes model is built for European options, it's blind to American options. Shockingly was still used on American options tho. To fix these issues the Cox-Ross-Rubenstein and Whaley model were developed to better model these differences.
## Hedging
Most basic form of hedging is hedging delta, your directional exposure. If you have a directional position already, often people will buy a call or put to cap the directional exposure. Or even if they're feeling spicy will do a fence, which caps both up and downside. How nice!
## More volatility
How do we accurately guess what volatility is for an option, so we can price it?

One useful characteristic of volatility is that it seems to be mean reverting. If you plot volatility over time it seems to hover up and down around a value even if the price of the security is trending upwards.

ARCH, GARCH are just volatility models. Encodes stuff like for long term options we want to use long term volatility and for short term options we should use recent volatility.
## Stock index futures and options
Indexes allow people to invest in the market as a whole. If indices are mispriced you can do an index arbitrage, buy correcting the index to the underlying securities.

Of course you can handle the difficulty of doing an index arb by hitting the index and hitting the underlying securities but you can also try and hit a proxy for the underlying securities instead. Such as a basket of highly correlated stocks instead. Nice!
## Inter-market spreading
If you can identify a relationship between two things across markets you can make money off them!

If we're comparing things across market we need to know the delta they represent and somehow compare the two. To do this we use dollar delta, delta multiplied by the dollar value to get the dollar exposure your security actually gives you.
- You can also get the equivalent dollar gamma, theta, vega as well. So you can exploit these across markets as well.

## Position analysis
How do you analyse the risk of your existing positions?

First thing you might think of is looking at is the risk sensitivities of the position (delta, gamma, theta, vega, rho), but these are only useful under the narrowly defined market conditions.
## Models and the real world
There are two things you gotta know
1. Your model might have the wrong assumptions
2. You might be feeding bad data into the model

Here's some assumptions that are made with traditional pricing models.
1. Markets are frictionless
	1. You can buy and sell stuff (e.g Not blocked from shorting, don't have price limits to movements as future markets do)
	2. No taxes!
	3. Anyone can borrow freely, same interest rate for everyone (You might get margin called)
	4. No transaction costs
2. Interests rates are constant over an option
3. Volatility is constant over an option (Volatility is not constant, you can model volatility is stochastic)
4. Trading is continuous, theres no price gaps between prices (Can model prices as jump processes and as diffusion processes)
5. Volatility is independent to price (It seems that depending on the market, when prices move up or down theres an inclination for one direction to impact the volatility. You can model this with constant elasticity of variance CEV model)
6. Over short time spans, percent changes of underlying contract are normal distribution, and therefore prices are log normally distributed (Nope, slightly different, has a bit more mean and outlier datapoints. You can model this with skew and kurtosis)