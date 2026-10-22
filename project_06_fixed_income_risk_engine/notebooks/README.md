# Fixed Income Analytics, Yield Curve Modelling & Portfolio Risk Engine

An educational Python project for analysing interest-rate risk in a synthetic US Treasury portfolio. The notebook connects bond cash-flow valuation and sensitivity measures with historical yield-curve analysis, portfolio-level risk estimates, out-of-sample-style VaR exception diagnostics, and stress testing.

> **Scope:** This is a research and learning project, not a production pricing or risk system. The portfolio is synthetic, and several curve and backtesting components rely on explicitly stated simplifying assumptions.

## Project Objectives

- Explore historical US Treasury par yields across short-, intermediate-, and long-term maturities.
- Price regular-coupon bonds using face value, coupon rate, maturity, yield to maturity (YTM), and coupon frequency.
- Calculate Macaulay duration, modified duration, DV01, and convexity.
- Compare duration-based price estimates with full bond repricing under yield shocks.
- Interpolate the observed par-yield curve and construct an **approximate, assumption-driven** spot curve.
- Use Principal Component Analysis (PCA) to study common patterns in standardized daily yield changes.
- Aggregate market value, duration, and DV01 across an illustrative four-bond portfolio.
- Estimate Historical Value at Risk (VaR) and Expected Shortfall (ES) from historical yield-change scenarios.
- Run rolling VaR exception analysis, a Kupiec Proportion-of-Failures (POF) test, and parallel/non-parallel stress scenarios.

## Notebook

The main deliverable is [`06_fixed_income_risk_engine_reviewed.ipynb`](06_fixed_income_risk_engine_reviewed.ipynb).

The notebook is organised as a sequence from data inspection and bond pricing through sensitivity measurement, yield-curve analysis, PCA, portfolio aggregation, VaR/ES, backtesting, stress testing, and a final findings section.

## Data

The notebook reads a local CSV file named:

`data/raw/par-yield-curve-rates-1990-2023.csv`

It selects six Treasury par-yield series:

| CSV maturity | Notebook label |
|---|---|
| 3-month | 3M |
| 1-year | 1Y |
| 2-year | 2Y |
| 5-year | 5Y |
| 10-year | 10Y |
| 30-year | 30Y |

Although the file contains older history, the notebook analysis uses observations after January 1, 2010. In the current dataset, the sample ends on December 29, 2023.

**Data units matter:** the raw CSV yields are in percentage points (for example, `4.25` means 4.25%). The notebook converts yields to decimals where needed. Daily changes from percentage-point data are multiplied by 100 to express them in basis points (bps). One basis point is 0.01 percentage point, or 0.0001 in decimal-yield units.

The CSV should be placed at the path above relative to the directory from which the notebook is run. The notebook currently uses a Windows-style relative path in its `read_csv` call; on macOS/Linux, change that path to `data/raw/par-yield-curve-rates-1990-2023.csv` or use `pathlib.Path` for cross-platform path handling.

## Setup and Run

### 1. Set up the project directory

Ensure the notebook and data file are arranged as follows:

```text
project-root/
├── README.md
├── 06_fixed_income_risk_engine_reviewed.ipynb
└── data/
    └── raw/
        └── par-yield-curve-rates-1990-2023.csv
```

### 2. Install the dependencies

Use Python 3.10+ and install the libraries used by the notebook:

```bash
python -m pip install numpy pandas matplotlib scipy scikit-learn jupyter
```

### 3. Launch Jupyter

From the project root, run:

```bash
jupyter lab
```

Open `06_fixed_income_risk_engine_reviewed.ipynb` and run the cells from top to bottom. The data file must be available at the expected relative path. The analysis uses a local CSV snapshot and does not download new data automatically.

## Methodology and Workflow

1. **Data preparation and exploration** — load and align the six Treasury par-yield series, inspect the time series, and plot the latest observed curve.
2. **Bond valuation** — discount regular coupon payments and principal using a nominal annual YTM compounded at the coupon frequency.
3. **Interest-rate sensitivity** — calculate Macaulay duration, modified duration, DV01, and convexity; compare approximation methods with full repricing.
4. **Yield-curve interpolation and approximate bootstrapping** — interpolate observed par yields and derive an illustrative spot curve under simplified assumptions.
5. **PCA** — fit PCA to standardized daily changes in the six yield series and inspect explained variance and component loadings.
6. **Synthetic portfolio** — value $1 million face-value positions at 2Y, 5Y, 10Y, and 30Y maturities and aggregate market value, duration, and DV01.
7. **Historical scenario P&L and tail risk** — apply historical changes in the corresponding 2Y, 5Y, 10Y, and 30Y par-yield series to fixed reference bond yields; fully reprice positions to build a scenario P&L distribution, then calculate VaR and ES.
8. **Rolling VaR diagnostics** — estimate thresholds on a 500-observation historical window and evaluate the next scenario observation, then apply the Kupiec POF test to the resulting exception flags.
9. **Stress testing** — fully reprice the portfolio under parallel yield shifts and stylized non-parallel yield-curve scenarios.
10. **Consolidated findings** — summarise the portfolio measures, tail-risk statistics, stress results, backtesting diagnostics, and model limitations.

## Selected Results

The following figures reflect the notebook's current outputs and assumptions; they are examples from the synthetic portfolio, not forecasts or guaranteed loss bounds.

### Portfolio sensitivity

| Metric | Result |
|---|---:|
| Aggregate market value | Approximately $4.094 million |
| Market-value-weighted modified duration | Approximately 8.06 years |
| Portfolio DV01 | Approximately $3,299 per bp |

DV01 is the approximate dollar sensitivity to a **parallel 1 bp move across the portfolio's bond yields**. The position-level DV01s can also be used to assess individual yield shocks; total DV01 alone does not describe non-parallel curve risk.

### Historical scenario VaR and Expected Shortfall

| Confidence level | Historical VaR | Expected Shortfall |
|---|---:|---:|
| 95% | Approximately $26,159 | Approximately $35,421 |
| 99% | Approximately $40,476 | Approximately $50,235 |

These statistics are estimated from a constructed scenario P&L series: observed daily changes in the relevant par yields are applied to fixed reference yields and fixed synthetic holdings. They are **not** actual realised historical P&L for a portfolio held through 2010–2023.

### PCA

PCA is fitted to standardised daily changes across 3M, 1Y, 2Y, 5Y, 10Y, and 30Y. In the current sample, the first three components explain approximately 94.98% of standardised variation; the first four explain approximately 98.41%. The components are descriptive statistical factors and are not directly dollar risk factors in this implementation.

### Stress scenarios

- A parallel **+200 bps** shift produces a loss of approximately **$565,907**.
- A parallel **−200 bps** shift produces a gain of approximately **$788,430**.
- Among the specified non-parallel scenarios, the **long-end shock** produces the largest loss, approximately **$219,362**.

These outcomes depend on the scenario definitions, portfolio assumptions, and full-repricing model. The scenarios are stylized and should not be interpreted as probabilities or worst-case bounds.

### Kupiec POF diagnostic

The rolling exception analysis uses 3,001 observations:

| Metric | 95% VaR | 99% VaR |
|---|---:|---:|
| Exceptions | 161 | 42 |
| Target exception rate | 5.00% | 1.00% |
| Observed exception rate | 5.36% | 1.40% |
| P-value | 0.3645 | 0.0380 |
| Reject target rate at 5% significance? | No | Yes |

The POF test does not reject the 95% target exception rate, but rejects the 99% target rate at the 5% significance level. It tests unconditional exception frequency only; it does not test whether exceptions are clustered over time. The diagnostic concerns the constructed rolling scenario-P&L series, not independently observed historical portfolio P&L.

## Important Assumptions and Limitations

- **Synthetic holdings:** the four bond positions are illustrative and do not represent actual trades or a managed historical portfolio.
- **Simplified bond pricing:** the model assumes regular coupon periods and nominal YTM compounding at the coupon frequency. Settlement dates, accrued interest, clean/dirty price conventions, day-count conventions, holidays, and irregular coupon periods are not modelled.
- **Par yields are not spot rates:** the dataset contains six par-yield tenors. The approximate bootstrap uses interpolated par yields and assumed semiannual par-bond cash flows; it is not calibrated to actual Treasury bill and coupon-bond prices and is not an official zero-coupon curve.
- **No genuine key rate duration yet:** the finite-difference routine bumps one bond's single YTM. True key rate duration requires curve-based pricing and independent shocks to individual curve nodes.
- **Scenario P&L is not realised P&L:** historical yield changes are applied to fixed reference yields and fixed holdings. That gives a consistent historical shock distribution, but not the realised P&L of a portfolio continuously revalued through the historical period.
- **Backtesting scope:** the rolling window separates VaR estimation observations from the next scenario observation, but the entire P&L series still comes from the fixed-reference scenario construction. The Kupiec POF test does not check independence or conditional coverage.
- **Not implemented:** market-calibrated zero-coupon bootstrapping, parametric VaR, Monte Carlo VaR, PCA-factor portfolio VaR, dynamic hedging, and Christoffersen conditional-coverage testing are potential extensions rather than features of this notebook.

## Future Improvements

Potential next steps to make the analysis more market-realistic include:

- Build a calibrated discount curve from appropriate Treasury instrument prices or use a published zero-coupon curve.
- Implement true curve-node key rate duration and curve-shock repricing.
- Use a rolling, time-varying portfolio valuation or independent realised P&L for stronger VaR validation.
- Add exception-independence and conditional-coverage tests.
- Compare historical simulation with parametric and Monte Carlo VaR/ES.
- Add unit tests and checks for pricing conventions, yield units, and portfolio aggregation.

## License and Data Attribution

No license or data-redistribution permission is specified here. Add the applicable project license and the original dataset source/attribution before publishing or redistributing the repository.
