---
layout: post
tags:
  - Trading
---
## Bachelier


## Black scholes model
![](https://www.gstatic.com/education/formulas2/553212783/en/black_scholes_model.svg)

Basic intuition
1. `N(d1)St`: Return: The value of the stock you receive contingent on the option finishing in the memory.
2. `N(d2)Ke-rt`: Cost: This is just the probability that the option hits timed by the exercise price, discounted back to now.
3. `d2` represents the probability that the option will be exercised
4. `d1` hedge ratio of an option: its the distance of stock price from strike over normalised vol time
5. `Ke-rt` just how much we get if we exercise the option

## Black 76
Why have a black scholes model for commodities? It has fall backs.
1. theres a risk free interest rate
2. underlying follows brownian motion
	1. But vol and drift are considered constants!
3. no dividends
4. No arbs
5. No transaction costs

Noticed that BSM didn't work for commodities. Agricultural product underlying rise before harvest and fall after, oil usually rises during winter and falls during summer.

So just use BSM for futures instead of pointing it directly at the underlying spot.

![](https://www.glynholton.com/wp-content/uploads/2013/04/formua_black_1976_1.png)
![](https://www.glynholton.com/wp-content/uploads/2013/04/formua_black_1976_3.png)
![](https://www.glynholton.com/wp-content/uploads/2013/04/formua_black_1976_4.png)

Honestly not that different.
## Appendix

BSM
- <https://brilliant.org/wiki/black-scholes-merton/>
- <https://www.investopedia.com/terms/b/blackscholes.asp>
- <https://financetrainingcourse.com/education/wp-content/uploads/2011/03/Understanding.pdf>
- <https://gregorygundersen.com/blog/2024/09/28/black-scholes/>
- <https://benjaminwhiteside.com/2021/01/15/black-76/>
- <https://www.researchgate.net/publication/228318867_An_Intuitive_Understanding_of_the_Black-Scholes_Formulas >
- <https://notion.moontowermeta.com/the-intuition-behind-the-black-scholes-equation>

B76
- <https://www.glynholton.com/notes/black_1976/>
- <https://eumaeus.org/wordp/index.php/2018/08/27/why-black-76/>