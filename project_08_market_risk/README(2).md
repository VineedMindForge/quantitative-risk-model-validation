# Market Risk Analysis

## Overview

This project explores foundational market-risk measurement using
historical financial market data. The notebook walks through return
calculations, basic risk statistics, time-series dependence, drawdowns,
and Value at Risk (VaR).

The project is intended as a documented learning exercise
in market-risk analysis. It focuses on understanding the calculations
and interpreting their outputs rather than building a production risk
system.

## Objectives

-   Calculate daily and month-end asset returns from price data.
-   Measure return variance.
-   Examine serial dependence using autocorrelation and partial
    autocorrelation.
-   Quantify historical drawdowns.
-   Estimate Value at Risk using historical and parametric approaches.
-   Explain the assumptions and limitations behind the results.

## Notebook

  -----------------------------------------------------------------------
  File                                Description
  ----------------------------------- -----------------------------------
  `01_single_asset_market_risk_analysis.ipynb`     Main notebook containing the
                                      analysis, calculations,
                                      visualizations, and explanatory
                                      Markdown.

  -----------------------------------------------------------------------


## Topics Covered

### 1. Price Data and Returns

The notebook works with historical price data and derives daily and
month-end returns. Returns provide a more useful basis for comparing
risk over time than raw price changes alone.

### 2. Variance

Return variance measures dispersion around the mean. The notebook
considers the distinction between sample and population variance,
including the effect of the degrees-of-freedom setting.

### 3. Autocorrelation and Partial Autocorrelation

Autocorrelation (ACF) helps identify relationships between returns at
different lags. Partial autocorrelation (PACF) estimates the
relationship at a given lag after accounting for shorter lags. These
diagnostics can help assess whether returns exhibit serial dependence.

### 4. Drawdown Analysis

Drawdown measures the decline from a previous cumulative-wealth peak.
Maximum drawdown summarizes the largest peak-to-trough decline over the
period examined. It provides a complementary view of downside experience
that is not captured by variance alone.

### 5. Historical Value at Risk

Historical VaR estimates a loss threshold from the empirical
distribution of observed returns. At the 95% confidence level, the
estimate is based on the lower tail of the return distribution. It does
not imply that losses beyond the threshold are impossible.

### 6. Parametric Value at Risk

Parametric VaR estimates risk using distributional assumptions and
estimated return statistics. The normal-distribution approach is
computationally convenient, but results depend on the adequacy of those
assumptions. Rolling estimates can show how measured risk changes over
time.

## Methodological Considerations

-   **Historical data:** Estimates depend on the selected asset, sample
    period, data quality, and return frequency.
-   **Distributional assumptions:** Parametric VaR may understate tail
    risk when returns are skewed or have heavy tails.
-   **Historical VaR:** The historical method assumes past observations
    are informative about the risk being estimated; it may not capture
    unprecedented market conditions.
-   **VaR limitation:** VaR does not describe the average or severity of
    losses beyond its threshold. Expected Shortfall is a natural
    extension.
-   **Risk scope:** This notebook focuses on a single-asset/foundational
    analysis. It is not a complete portfolio-risk engine and does not
    currently implement portfolio risk attribution, stress testing, or
    VaR backtesting.

## Disclaimer

This project is for educational and portfolio-demonstration purposes
only. The analysis is not investment advice and should not be treated as
a production-grade risk-management system.
