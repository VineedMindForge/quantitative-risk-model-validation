"""
Generate consolidated results for Project 01 - Market Risk Engine.

This script replaces the exploratory 07_generate_results.ipynb notebook.
It generates:
    results/csv/
        portfolio_summary.csv
        volatility_summary.csv
        correlation_matrix.csv
        risk_contribution.csv
        var_comparison.csv
        expected_shortfall.csv

    results/figures/
        risk_contribution.png
        portfolio_return_distribution.png
        var_method_comparison.png

Run from the project root:
    python scripts/generate_results.py
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm


# ---------------------------------------------------------------------------
# Project setup
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data import download_prices
from src.var import (
    historical_var,
    historical_expected_shortfall,
    parametric_var,
    monte_carlo_var,
    monte_carlo_es,
)


RESULTS_DIR = PROJECT_ROOT / "results"
CSV_DIR = RESULTS_DIR / "csv"
FIGURE_DIR = RESULTS_DIR / "figures"

CSV_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Portfolio definition
# ---------------------------------------------------------------------------

PORTFOLIO = {
    "SPY": 0.30,
    "QQQ": 0.20,
    "IWM": 0.15,
    "TLT": 0.20,
    "GLD": 0.15,
}

START_DATE = "2015-01-01"
END_DATE = "2026-01-01"

PORTFOLIO_VALUE = None
N_SIMULATIONS = 100_000
RANDOM_SEED = 42


# ---------------------------------------------------------------------------
# Data preparation
# ---------------------------------------------------------------------------

def prepare_data():
    """Download price data and calculate daily asset returns."""

    portfolio_summary = pd.DataFrame({
        "ticker": list(PORTFOLIO.keys()),
        "weight": list(PORTFOLIO.values()),
    })

    prices = download_prices(
        tickers=portfolio_summary["ticker"].to_list(),
        start=START_DATE,
        end=END_DATE,
    )

    returns = prices.pct_change().dropna()

    weights = portfolio_summary.set_index("ticker")["weight"]

    return portfolio_summary, returns, weights


# ---------------------------------------------------------------------------
# CSV result generation
# ---------------------------------------------------------------------------

def generate_summary_results(portfolio_summary, returns):
    """Generate portfolio, volatility, and correlation CSV files."""

    portfolio_summary.to_csv(
        CSV_DIR / "portfolio_summary.csv",
        index=False,
    )

    annualized_volatility = returns.std() * np.sqrt(252)

    volatility_summary = (
        annualized_volatility
        .rename("annualized_volatility")
        .reset_index()
    )

    volatility_summary.columns = [
        "ticker",
        "annualized_volatility",
    ]

    volatility_summary.to_csv(
        CSV_DIR / "volatility_summary.csv",
        index=False,
    )

    correlation_matrix = returns.corr()

    correlation_matrix.to_csv(
        CSV_DIR / "correlation_matrix.csv"
    )


def generate_risk_contribution(returns, weights):
    """Calculate and save component risk contributions."""

    # Align returns to the portfolio weight order.
    aligned_returns = returns[weights.index]

    covariance_matrix = aligned_returns.cov()

    portfolio_volatility = np.sqrt(
        weights.T @ covariance_matrix @ weights
    )

    marginal_risk = (
        covariance_matrix @ weights
    ) / portfolio_volatility

    component_risk = weights * marginal_risk

    risk_contribution_pct = (
        component_risk / portfolio_volatility
    )

    risk_contribution = pd.DataFrame({
        "ticker": weights.index,
        "weight": weights.values,
        "risk_contribution": risk_contribution_pct.values,
    })

    # Basic validation.
    if not np.isclose(
        component_risk.sum(),
        portfolio_volatility,
    ):
        raise ValueError("Component risk does not sum to portfolio risk.")

    if not np.isclose(
        risk_contribution_pct.sum(),
        1.0,
    ):
        raise ValueError("Risk contributions do not sum to 100%.")

    risk_contribution.to_csv(
        CSV_DIR / "risk_contribution.csv",
        index=False,
    )

    return risk_contribution, portfolio_volatility


def generate_var_results(returns, weights):
    """Calculate and save Historical, Parametric, and Monte Carlo VaR."""

    portfolio_returns = returns @ weights

    historical_var_95 = historical_var(
        portfolio_returns,
        confidence_level=0.95,
        portfolio_value=PORTFOLIO_VALUE,
    )

    historical_var_99 = historical_var(
        portfolio_returns,
        confidence_level=0.99,
        portfolio_value=PORTFOLIO_VALUE,
    )

    parametric_var_95 = parametric_var(
        portfolio_returns,
        confidence_level=0.95,
        portfolio_value=PORTFOLIO_VALUE,
    )

    parametric_var_99 = parametric_var(
        portfolio_returns,
        confidence_level=0.99,
        portfolio_value=PORTFOLIO_VALUE,
    )

    monte_carlo_var_95 = monte_carlo_var(
        returns,
        weights,
        confidence_level=0.95,
        portfolio_value=PORTFOLIO_VALUE,
        n_simulations=N_SIMULATIONS,
        random_seed=RANDOM_SEED,
    )

    monte_carlo_var_99 = monte_carlo_var(
        returns,
        weights,
        confidence_level=0.99,
        portfolio_value=PORTFOLIO_VALUE,
        n_simulations=N_SIMULATIONS,
        random_seed=RANDOM_SEED,
    )

    var_comparison = pd.DataFrame({
        "confidence_level": [0.95, 0.99],
        "historical_var": [
            historical_var_95,
            historical_var_99,
        ],
        "parametric_var": [
            parametric_var_95,
            parametric_var_99,
        ],
        "monte_carlo_var": [
            monte_carlo_var_95,
            monte_carlo_var_99,
        ],
    })

    var_comparison.to_csv(
        CSV_DIR / "var_comparison.csv",
        index=False,
    )

    return portfolio_returns, var_comparison


def generate_expected_shortfall(returns, weights, portfolio_returns):
    """Calculate and save Historical and Monte Carlo Expected Shortfall."""

    historical_es_95 = historical_expected_shortfall(
        portfolio_returns,
        confidence_level=0.95,
        portfolio_value=PORTFOLIO_VALUE,
    )

    historical_es_99 = historical_expected_shortfall(
        portfolio_returns,
        confidence_level=0.99,
        portfolio_value=PORTFOLIO_VALUE,
    )

    monte_carlo_es_95 = monte_carlo_es(
        returns,
        weights,
        confidence_level=0.95,
        portfolio_value=PORTFOLIO_VALUE,
        n_simulations=N_SIMULATIONS,
        random_seed=RANDOM_SEED,
    )

    monte_carlo_es_99 = monte_carlo_es(
        returns,
        weights,
        confidence_level=0.99,
        portfolio_value=PORTFOLIO_VALUE,
        n_simulations=N_SIMULATIONS,
        random_seed=RANDOM_SEED,
    )

    expected_shortfall = pd.DataFrame({
        "confidence_level": [0.95, 0.99],
        "historical_es": [
            historical_es_95,
            historical_es_99,
        ],
        "monte_carlo_es": [
            monte_carlo_es_95,
            monte_carlo_es_99,
        ],
    })

    expected_shortfall.to_csv(
        CSV_DIR / "expected_shortfall.csv",
        index=False,
    )

    return expected_shortfall


# ---------------------------------------------------------------------------
# Figure generation
# ---------------------------------------------------------------------------

def generate_risk_contribution_figure(risk_contribution):
    """Generate portfolio weight versus risk contribution figure."""

    x = np.arange(len(risk_contribution))
    width = 0.35

    plt.figure(figsize=(10, 6))

    plt.bar(
        x - width / 2,
        risk_contribution["weight"] * 100,
        width,
        label="Portfolio Weight",
    )

    plt.bar(
        x + width / 2,
        risk_contribution["risk_contribution"] * 100,
        width,
        label="Risk Contribution",
    )

    plt.xticks(x, risk_contribution["ticker"])
    plt.ylabel("Percentage (%)")
    plt.xlabel("Asset")
    plt.title("Portfolio Weight vs. Risk Contribution")
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "risk_contribution.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def generate_return_distribution_figure(portfolio_returns):
    """Generate observed portfolio return distribution versus normal density."""

    mu = portfolio_returns.mean()
    sigma = portfolio_returns.std()

    x = np.linspace(
        portfolio_returns.min(),
        portfolio_returns.max(),
        500,
    )

    normal_density = norm.pdf(
        x,
        mu,
        sigma,
    )

    plt.figure(figsize=(10, 6))

    plt.hist(
        portfolio_returns,
        bins=60,
        density=True,
        alpha=0.7,
        label="Observed Returns",
    )

    plt.plot(
        x,
        normal_density,
        linewidth=2,
        label="Normal Distribution",
    )

    plt.xlabel("Daily Portfolio Return")
    plt.ylabel("Density")
    plt.title("Portfolio Return Distribution vs. Normal Distribution")
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "portfolio_return_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def generate_var_comparison_figure(var_comparison):
    """Generate comparison of the three VaR methodologies."""

    x = np.arange(len(var_comparison))
    width = 0.25

    plt.figure(figsize=(10, 6))

    plt.bar(
        x - width,
        var_comparison["historical_var"] * 100,
        width,
        label="Historical",
    )

    plt.bar(
        x,
        var_comparison["parametric_var"] * 100,
        width,
        label="Parametric",
    )

    plt.bar(
        x + width,
        var_comparison["monte_carlo_var"] * 100,
        width,
        label="Monte Carlo",
    )

    plt.xticks(x, ["95%", "99%"])
    plt.ylabel("One-Day VaR (%)")
    plt.xlabel("Confidence Level")
    plt.title("Comparison of VaR Methodologies")
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        FIGURE_DIR / "var_method_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def main():
    """Generate all consolidated project results."""

    print("Generating Project 01 results...")

    portfolio_summary, returns, weights = prepare_data()

    generate_summary_results(
        portfolio_summary,
        returns,
    )

    risk_contribution, portfolio_volatility = generate_risk_contribution(
        returns,
        weights,
    )

    portfolio_returns, var_comparison = generate_var_results(
        returns,
        weights,
    )

    expected_shortfall = generate_expected_shortfall(
        returns,
        weights,
        portfolio_returns,
    )

    generate_risk_contribution_figure(
        risk_contribution,
    )

    generate_return_distribution_figure(
        portfolio_returns,
    )

    generate_var_comparison_figure(
        var_comparison,
    )

    print(f"Portfolio volatility: {portfolio_volatility:.6%}")
    print(
        f"Historical VaR 95%:   "
        f"{var_comparison.loc[0, 'historical_var']:.6%}"
    )
    print(
        f"Historical VaR 99%:   "
        f"{var_comparison.loc[1, 'historical_var']:.6%}"
    )
    print(
        f"Historical ES 95%:    "
        f"{expected_shortfall.loc[0, 'historical_es']:.6%}"
    )
    print(
        f"Historical ES 99%:    "
        f"{expected_shortfall.loc[1, 'historical_es']:.6%}"
    )

    print("Results generated successfully.")


if __name__ == "__main__":
    main()
