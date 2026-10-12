# Quantitative Risk & Model Validation Portfolio

A collection of four Python-based projects exploring **market risk, derivatives pricing, credit risk, and volatility-model validation**. Each project moves from data preparation and quantitative implementation to interpretation of results, diagnostics, stress testing, and explicit discussion of model limitations.

> **Scope:** These are research and portfolio projects designed to demonstrate quantitative-risk methods and model assessment. They are not production risk systems, independently approved models, investment recommendations, or credit-decision tools.

## Projects

### 01 — Market Risk Engine

**Focus:** Portfolio market risk, tail-risk measurement, risk attribution, stress testing, and VaR validation.

Builds a fixed-weight ETF portfolio from daily market data and compares Historical, Parametric, and Monte Carlo Value at Risk (VaR), alongside Expected Shortfall (ES). The analysis also examines volatility and correlations, decomposes risk contributions, applies deterministic stress scenarios, and tests rolling VaR forecasts against realized losses.

**Selected findings:** Annualized portfolio volatility is **12.84%** in the recorded sample. The three VaR approaches are relatively close at 95% confidence but diverge at 99%; the Kupiec exception-frequency test rejects all three models at the 99% level.

**Methods demonstrated:** Return construction, covariance-based portfolio risk, rolling and EWMA volatility, Historical/Parametric/Monte Carlo VaR, Expected Shortfall, Marginal and Component VaR, stress testing, and backtesting.

[Read the Project 01 README](project_01_market_risk_engine/README.md)

---

### 02 — Black-Scholes, Greeks & Derivatives Risk Engine

**Focus:** Option valuation, risk sensitivities, implied volatility, and nonlinear portfolio stress testing.

Uses a SPY option-chain snapshot to compare Black-Scholes prices with market midpoints, calculate Delta, Gamma, Vega, Theta, and Rho, estimate implied volatility, and analyze an illustrative six-position options portfolio. It compares Greek-based P&L approximations with full Black-Scholes revaluation under underlying-price, volatility, and time-decay shocks.

**Selected findings:** The saved option-chain sample contains **256 contracts**. The implied-volatility solver returned valid values for **147 contracts (57.4%)**; the remaining failures and sizeable deviations from provider IV are important diagnostics, not results to conceal. For the illustrative portfolio, the Delta–Gamma approximation diverges materially from full repricing over the tested price-shock range.

**Methods demonstrated:** Black-Scholes pricing, market-price diagnostics, numerical root finding, implied-volatility analysis, Greeks aggregation, scenario P&L, and full-revaluation comparison.

[Read the Project 02 README](project_02_derivatives_risk_engine/README.md)

---

### 03 — Credit Risk: PD, LGD, EAD & Expected Loss

**Focus:** Consumer-credit default-risk estimation and expected-loss aggregation.

Uses LendingClub loan-performance data to prepare a terminal-outcome target, train a logistic-regression Probability of Default (PD) model, define transparent LGD assumptions and an EAD proxy, calculate loan-level expected loss, segment portfolio risk, and test PD sensitivity under moderate and severe stresses.

**Selected findings:** The out-of-time PD model achieves **ROC-AUC 0.6969**. Mean predicted PD is **18.26%**, compared with an observed validation charge-off rate of **22.47%**, a calibration gap of **+4.21 percentage points**. The expected-loss calculation is arithmetically reconciled, but LGD is assumption-based and original funded amount is used as an EAD proxy; the resulting dollar estimates are illustrative, not validated realized-loss forecasts.

**Methods demonstrated:** Chronological validation, logistic regression, discrimination and calibration assessment, risk bands, loan-level `PD × LGD × EAD`, portfolio segmentation, stress testing, and reconciliation checks.

[Read the Project 03 README](project_03_credit_risk/README.md)

---

### 04 — Volatility Model Validation & Challenger Analysis

**Focus:** Out-of-sample volatility forecasting and statistical comparison of competing models.

Compares rolling 60-day variance and EWMA forecasts with a GARCH(1,1) challenger for SPY daily returns. The workflow includes chronological train/test separation, one-day-ahead forecast alignment, forecast-loss scoring, volatility-regime analysis, GARCH residual diagnostics, and pairwise statistical comparisons with Holm adjustment.

**Selected findings:** EWMA has the lowest overall **MSE**, while GARCH(1,1) has the lowest overall **QLIKE**. None of the pairwise loss differences is statistically significant after Holm adjustment, so the evidence supports retaining EWMA as the practical benchmark and GARCH(1,1) as a challenger rather than declaring a definitive winner.

**Methods demonstrated:** Rolling variance, EWMA, GARCH(1,1), MSE and QLIKE scoring, residual and ARCH diagnostics, HAC-based forecast-loss comparisons, and multiple-comparison adjustment.

[Read the Project 04 README](project_04_volatility_model_validation/README.md)

---

## Capabilities demonstrated across the portfolio

- **Data preparation and validation:** data-quality checks, feature construction, return calculations, and chronological sample design.
- **Quantitative modeling:** market-risk measurement, option pricing, credit-risk estimation, and conditional-volatility forecasting.
- **Risk analysis:** portfolio aggregation, tail-loss measurement, sensitivity analysis, risk segmentation, and scenario stress testing.
- **Model assessment:** out-of-sample evaluation, calibration and residual diagnostics, backtesting, statistical comparisons, and explicit treatment of limitations.
- **Communication:** documented assumptions, interpretable quantitative results, visual analysis, and reproducible notebook-based workflows.

## How the projects fit together

The four projects examine related but distinct risk questions:

| Risk question | Project |
|---|---|
| How much could a multi-asset portfolio lose, and how well do VaR estimates perform? | **01 — Market Risk Engine** |
| How do option values and portfolio risk change as market inputs move? | **02 — Derivatives Risk Engine** |
| How can borrower-level PD, LGD, and EAD assumptions be combined into portfolio expected loss? | **03 — Credit Risk** |
| Which volatility forecast performs best out of sample, and is the performance difference statistically persuasive? | **04 — Volatility Model Validation** |

Together, they demonstrate an end-to-end perspective on quantitative risk: constructing inputs, implementing models, measuring risk, testing behavior under stress or out of sample, and distinguishing numerical results from evidence of model validity.

## Important limitations

The results depend on the datasets, assumptions, and implementations documented in each project. Several components are deliberately simplified—for example, the derivatives portfolio and shock grid are illustrative, the credit project uses assumption-based LGD and an EAD proxy, and the market-risk and volatility projects expose limitations in extreme-tail performance and model comparison. These limitations are part of the analysis and should be considered before interpreting the results for real-world decisions.
