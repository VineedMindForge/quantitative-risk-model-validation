# Risk vs. Return: Volatility and Portfolio Optimization

This notebook explores how volatility affects investment growth and how
different objectives lead to different portfolio allocations.

## 1. Same Return, Different Volatility

Two synthetic investments are simulated with the same assumed average
daily return but different daily volatility. Their cumulative growth and
return distributions are compared.

![Growth of \$1 for investments with different
volatility](figures/volatility_growth_comparison.png)

![Daily return distributions for the two
investments](figures/return_distributions.png)

## 2. Historical Portfolio Analysis

Historical daily adjusted prices for **AAPL, MSFT, and AMZN** from
2019--2023 are used to estimate returns, volatility, and market betas
(using SPY as the market proxy).

The notebook optimizes portfolios for: - Maximum expected return -
Minimum variance - Maximum Sharpe ratio - Maximum Sortino ratio -
Maximum Treynor ratio

The portfolios are long-only, with weights constrained to sum to 100%.

## 3. Feasible Portfolios and Efficient Frontier

Five thousand random portfolios are generated to visualize the feasible
risk-return combinations. The optimized portfolios are overlaid for
comparison. Risk is measured by annualized volatility, and the color
scale represents the Sharpe ratio.

![Feasible portfolio set and optimized
portfolios](figures/efficient_frontier.png)

## Tools and Methods

Python, pandas, NumPy, Matplotlib, SciPy, and yfinance. Daily returns
are used to estimate annualized return and risk using 252 trading days.

## Note

Results depend on the selected historical period and assumptions. They
are educational illustrations, not investment recommendations.
