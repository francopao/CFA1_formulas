# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 01:19:02 2026

@author: usuario
"""

import streamlit as st
import random
import time

st.set_page_config(page_title="CFA Formula Trainer", layout="centered")

# -------------------------------------------------
# BANCO DE FORMULAS
# -------------------------------------------------

FORMULAS = [
    {
        "id": "HPR",
        "question": "You are given opening price, closing price, and dividend. Which return measure should you use?",
        "formula": "(Closing Price − Opening Price + Income) / Opening Price",
        "trap": "Forgetting to include income (dividends or coupons)."
    },
    {
        "id": "MULTI_HPR",
        "question": "You want the total return over several years with compounding.",
        "formula": "(1+R1)(1+R2)...(1+Rn) − 1",
        "trap": "Using arithmetic mean instead of compounding."
    },
    {
        "id": "ARITH_MEAN",
        "question": "You want the expected return over one period.",
        "formula": "Arithmetic Mean = ΣRi / n",
        "trap": "Using geometric mean for expectation."
    },
    {
        "id": "GEOM_MEAN",
        "question": "You want the average compounded growth rate over time.",
        "formula": "Geometric Mean = [(1+R1)...(1+Rn)]^(1/n) − 1",
        "trap": "Using arithmetic mean for multi-period returns."
    },
    {
        "id": "HARM_MEAN",
        "question": "You are averaging ratios (e.g. valuation multiples).",
        "formula": "Harmonic Mean = n / (1/x1 + 1/x2 + ... + 1/xn)",
        "trap": "Using arithmetic mean for ratios."
    },
    {
        "id": "MWRR",
        "question": "Portfolio return affected by investor-controlled cash flows.",
        "formula": "IRR solving: Σ CF_t / (1+IRR)^t = 0",
        "trap": "Confusing with time-weighted return."
    },
    {
        "id": "TWRR",
        "question": "You want manager performance independent of cash flow timing.",
        "formula": "Geometric mean of all holding period returns",
        "trap": "Using IRR instead of geometric mean."
    },
    
    # -------------------------------
    # SOLVENCY / LEVERAGE RATIOS
    # -------------------------------
    
    {
        "id": "DEBT_TO_EQUITY",
        "question": "You want to measure the proportion of debt relative to shareholders’ equity.",
        "formula": "Total Debt / Total Equity",
        "trap": "Using total liabilities instead of debt."
    },
    {
        "id": "DEBT_TO_ASSETS",
        "question": "You want to assess what portion of assets is financed with debt.",
        "formula": "Total Debt / Total Assets",
        "trap": "Confusing with debt-to-equity."
    },
    {
        "id": "DEBT_TO_CAPITAL",
        "question": "You want the percentage of permanent capital financed by debt.",
        "formula": "Debt / (Debt + Equity)",
        "trap": "Using total assets instead of capital."
    },
    {
        "id": "FINANCIAL_LEVERAGE",
        "question": "You want to assess balance sheet leverage using assets and equity.",
        "formula": "Average Assets / Average Equity",
        "trap": "Using end-of-period values instead of averages."
    },
    {
        "id": "INTEREST_COVERAGE",
        "question": "You want to assess a firm’s ability to service interest payments.",
        "formula": "EBIT / Interest Expense",
        "trap": "Using net income instead of EBIT."
    },
    
    # -------------------------------
    # LIQUIDITY RATIOS
    # -------------------------------
    
    {
        "id": "CURRENT_RATIO",
        "question": "You want to assess a company's ability to meet short-term obligations using all current assets.",
        "formula": "Current Assets / Current Liabilities",
        "trap": "Assuming higher is always better without considering asset quality."
    },
    {
        "id": "CASH_RATIO",
        "question": "You want the most conservative liquidity measure excluding receivables and inventory.",
        "formula": "(Cash + Marketable Securities) / Current Liabilities",
        "trap": "Including receivables or inventory."
    },
    {
        "id": "QUICK_RATIO",
        "question": "You want a liquidity ratio excluding inventory but including receivables.",
        "formula": "(Cash + Marketable Securities + Accounts Receivable) / Current Liabilities",
        "trap": "Confusing with cash ratio."
    },
    {
        "id": "DEFENSIVE_INTERVAL",
        "question": "You want to know how many days a company can operate using liquid assets only.",
        "formula": "(Cash + Marketable Securities + Accounts Receivable) / Average Daily Expenses",
        "trap": "Using current liabilities instead of daily expenses."
    },
    {
        "id": "CASH_CONVERSION_CYCLE",
        "question": "You want to measure how long cash is tied up in operations.",
        "formula": "Days Inventory Outstanding + Days Sales Outstanding − Days Payables Outstanding",
        "trap": "Adding days payables instead of subtracting."
    },
    
    # -------------------------------
    # PROFITABILITY RATIOS
    # -------------------------------
    
    {
        "id": "NET_PROFIT_MARGIN",
        "question": "You want to measure profitability after all expenses.",
        "formula": "Net Income / Sales",
        "trap": "Using EBIT instead of net income."
    },
    {
        "id": "GROSS_PROFIT_MARGIN",
        "question": "You want to assess profitability after cost of goods sold.",
        "formula": "Gross Profit / Sales",
        "trap": "Confusing with operating margin."
    },
    {
        "id": "OPERATING_MARGIN",
        "question": "You want operating profitability before financing and taxes.",
        "formula": "EBIT / Sales",
        "trap": "Using net income instead of EBIT."
    },
    {
        "id": "PRETAX_MARGIN",
        "question": "You want profitability before taxes but after interest.",
        "formula": "Earnings Before Tax / Sales",
        "trap": "Confusing with operating margin."
    },
    
    # --------------------------------
    # CAPITAL STRUCTURE & FIRM VALUE
    # --------------------------------
    
    {
        "id": "MARKET_CAP",
        "question": "You want to measure the market value of a firm's equity.",
        "formula": "Current Share Price × Total Shares Outstanding",
        "trap": "Using book value instead of market value."
    },
    {
        "id": "ENTERPRISE_VALUE",
        "question": "You want the total value of the firm independent of capital structure.",
        "formula": "Market Value of Equity + Market Value of Debt + Preferred Equity − Cash",
        "trap": "Forgetting to subtract cash."
    },
    
    # --------------------------------
    # WORKING CAPITAL & LIQUIDITY
    # --------------------------------
    
    {
        "id": "INVENTORY_TURNOVER",
        "question": "You want to measure how efficiently inventory is managed.",
        "formula": "COGS / Average Inventory",
        "trap": "Using sales instead of COGS."
    },
    {
        "id": "AR_TURNOVER",
        "question": "You want to assess how quickly receivables are collected.",
        "formula": "Credit Sales / Average Accounts Receivable",
        "trap": "Using total sales instead of credit sales."
    },
    {
        "id": "AP_TURNOVER",
        "question": "You want to assess how quickly a firm pays its suppliers.",
        "formula": "Credit Purchases / Average Accounts Payable",
        "trap": "Using COGS instead of purchases."
    },
    {
        "id": "DAYS_IN_INVENTORY",
        "question": "You want to know the average number of days inventory is held.",
        "formula": "365 / Inventory Turnover",
        "trap": "Using receivables turnover instead."
    },
    {
        "id": "DAYS_IN_RECEIVABLES",
        "question": "You want to know how long it takes to collect from customers.",
        "formula": "365 / Receivables Turnover",
        "trap": "Using inventory turnover."
    },
    {
        "id": "DAYS_IN_PAYABLES",
        "question": "You want to know how long the firm takes to pay suppliers.",
        "formula": "365 / Payables Turnover",
        "trap": "Adding instead of subtracting in CCC."
    },
    {
        "id": "CASH_CONVERSION_CYCLE_CF",
        "question": "You want to measure how long cash is tied up in operations.",
        "formula": "Days Inventory + Days Receivables − Days Payables",
        "trap": "Adding days payables instead of subtracting."
    },
    
    # --------------------------------
    # CASH FLOW DEFINITIONS
    # --------------------------------
    
    {
        "id": "CASH_FLOW_FROM_OPERATIONS",
        "question": "You want cash generated by core business operations.",
        "formula": "NI + Non-cash charges + Decrease in WC − Increase in WC",
        "trap": "Including financing cash flows."
    },
    {
        "id": "FREE_CASH_FLOW_FIRM",
        "question": "You want cash available to all capital providers.",
        "formula": "CFO − Capital Expenditures",
        "trap": "Confusing with FCFE."
    },
    
    # --------------------------------
    # CAPITAL BUDGETING
    # --------------------------------
    
    {
        "id": "NPV",
        "question": "You want to measure value added by an investment project.",
        "formula": "PV of Cash Inflows − PV of Cash Outflows",
        "trap": "Ignoring the time value of money."
    },
    {
        "id": "IRR",
        "question": "You want the discount rate that sets NPV equal to zero.",
        "formula": "Discount rate such that Σ CF_t / (1+IRR)^t = 0",
        "trap": "Multiple IRRs with non-conventional cash flows."
    },
    {
        "id": "PROFITABILITY_INDEX",
        "question": "You want value created per unit of investment.",
        "formula": "PV of Inflows / PV of Outflows",
        "trap": "Using NPV ranking instead of PI under capital rationing."
    },
    
    # --------------------------------
    # RETURN & VALUE CREATION
    # --------------------------------
    
    {
        "id": "ROIC",
        "question": "You want to measure return generated on invested capital.",
        "formula": "After-Tax Operating Profit / Average Invested Capital",
        "trap": "Using net income instead of operating profit."
    },
    {
        "id": "PROJECT_NPV_WITH_OPTION",
        "question": "You want project value including embedded real options.",
        "formula": "NPV (without option) + Option Value",
        "trap": "Ignoring managerial flexibility."
    },
    
    # --------------------------------
    # COST OF CAPITAL
    # --------------------------------
    
    {
        "id": "WACC",
        "question": "You want the firm’s overall required return.",
        "formula": "Wd·Rd·(1−T) + We·Re + Wp·Rp",
        "trap": "Forgetting the tax shield on debt."
    },
    {
        "id": "COST_OF_DEBT",
        "question": "You want the after-tax cost of debt.",
        "formula": "Yield to Maturity × (1 − Tax Rate)",
        "trap": "Using coupon rate instead of YTM."
    },
    {
        "id": "COST_OF_PREFERRED",
        "question": "You want the cost of preferred equity.",
        "formula": "Annual Preferred Dividend / Market Price of Preferred Stock",
        "trap": "Using book price instead of market price."
    },
    {
        "id": "CAPM",
        "question": "You want the required return on equity using systematic risk.",
        "formula": "Rf + β × (Rm − Rf)",
        "trap": "Using total risk instead of beta."
    },
    # --------------------------------
    # UTILITY, RISK & RETURN
    # --------------------------------
    
    {
        "id": "UTILITY_FUNCTION",
        "question": "You want to express investor preferences between return and risk.",
        "formula": "U = E(R) − 0.5·A·σ²",
        "trap": "Using variance instead of standard deviation squared."
    },
    {
        "id": "EXPECTED_RETURN_PORTFOLIO",
        "question": "You want the expected return of a portfolio.",
        "formula": "Σ wᵢ·E(Rᵢ)",
        "trap": "Using historical returns instead of expected returns."
    },
    {
        "id": "PORTFOLIO_VARIANCE_2_ASSETS",
        "question": "You want the risk of a two-asset portfolio.",
        "formula": "w₁²σ₁² + w₂²σ₂² + 2w₁w₂Cov(1,2)",
        "trap": "Ignoring covariance."
    },
    {
        "id": "COVARIANCE",
        "question": "You want a measure of joint movement between two assets.",
        "formula": "ρ₁₂·σ₁·σ₂",
        "trap": "Confusing covariance with correlation."
    },
    
    # --------------------------------
    # CORRELATION & DIVERSIFICATION
    # --------------------------------
    
    {
        "id": "CORRELATION",
        "question": "You want a standardized measure of dependence between assets.",
        "formula": "Cov(1,2) / (σ₁·σ₂)",
        "trap": "Forgetting correlation is bounded between −1 and +1."
    },
    {
        "id": "PORTFOLIO_SD_2_ASSETS",
        "question": "You want portfolio volatility using correlation.",
        "formula": "√(w₁²σ₁² + w₂²σ₂² + 2w₁w₂σ₁σ₂ρ₁₂)",
        "trap": "Omitting the square root."
    },
    {
        "id": "MINIMUM_VARIANCE_EFFECT",
        "question": "You want to reduce portfolio risk without reducing expected return.",
        "formula": "Diversification via low or negative correlation",
        "trap": "Assuming diversification depends only on number of assets."
    },
    
    # --------------------------------
    # SYSTEMATIC VS UNSYSTEMATIC RISK
    # --------------------------------
    
    {
        "id": "SYSTEMATIC_RISK",
        "question": "You want the portion of risk explained by market movements.",
        "formula": "β²·σ²_market",
        "trap": "Assuming it can be diversified away."
    },
    {
        "id": "UNSYSTEMATIC_RISK",
        "question": "You want the asset-specific risk component.",
        "formula": "Total Variance − Systematic Variance",
        "trap": "Assuming it is priced in equilibrium."
    },
    
    # --------------------------------
    # CAPITAL MARKET LINE (CML)
    # --------------------------------
    
    {
        "id": "CML_EQUATION",
        "question": "You want the expected return of an efficient portfolio.",
        "formula": "E(R) = Rf + [σp / σm]·(E(Rm) − Rf)",
        "trap": "Using beta instead of standard deviation."
    },
    {
        "id": "CML_SCOPE",
        "question": "You want to know which portfolios lie on the CML.",
        "formula": "Efficient portfolios combining Rf and market portfolio",
        "trap": "Including inefficient portfolios."
    },
    
    # --------------------------------
    # SECURITY MARKET LINE (SML)
    # --------------------------------
    
    {
        "id": "CAPM_EQUATION",
        "question": "You want the expected return of a risky asset.",
        "formula": "E(Rᵢ) = Rf + βᵢ·(E(Rm) − Rf)",
        "trap": "Using total risk instead of beta."
    },
    {
        "id": "SML_INTERPRETATION",
        "question": "You want to know if an asset is under or overvalued.",
        "formula": "Compare actual return vs CAPM expected return",
        "trap": "Comparing volatility instead of beta."
    },
    
    # --------------------------------
    # PERFORMANCE MEASURES
    # --------------------------------
    
    {
        "id": "SHARPE_RATIO",
        "question": "You want excess return per unit of total risk.",
        "formula": "(Rₚ − Rf) / σₚ",
        "trap": "Using beta instead of standard deviation."
    },
    {
        "id": "TREYNOR_RATIO",
        "question": "You want excess return per unit of systematic risk.",
        "formula": "(Rₚ − Rf) / βₚ",
        "trap": "Using total risk instead of beta."
    },
    {
        "id": "JENSENS_ALPHA",
        "question": "You want abnormal performance relative to CAPM.",
        "formula": "Rₚ − [Rf + βₚ(E(Rm) − Rf)]",
        "trap": "Ignoring beta adjustment."
    },
    {
        "id": "M_SQUARED",
        "question": "You want risk-adjusted performance in percentage terms.",
        "formula": "Rf + Sharpeₚ × σ_market",
        "trap": "Comparing raw returns instead of adjusted returns."
    },
    
    # --------------------------------
    # MULTIFACTOR MODELS
    # --------------------------------
    
    {
        "id": "MULTIFACTOR_MODEL",
        "question": "You want expected return using multiple sources of risk.",
        "formula": "E(R) = Rf + β₁F₁ + β₂F₂ + ... + βₙFₙ",
        "trap": "Assuming only market risk matters."
    },
    # --------------------------------
    # YIELD & DISCOUNT MEASURES
    # --------------------------------
    
    {
        "id": "DISCOUNT_RATE",
        "question": "You want the return measure based on face value, commonly used for T-bills.",
        "formula": "DR = (365 / Days) × (FV − Price) / FV",
        "trap": "Using price instead of face value in the denominator."
    },
    {
        "id": "ADD_ON_RATE",
        "question": "You want a money market yield based on the purchase price.",
        "formula": "AOR = (365 / Days) × (FV − Price) / Price",
        "trap": "Confusing it with discount rate."
    },
    
    # --------------------------------
    # TERM STRUCTURE & SPOT RATES
    # --------------------------------
    
    {
        "id": "PRESENT_VALUE_SPOT",
        "question": "You want to price a bond using spot rates.",
        "formula": "PV = Σ CFₜ / (1 + zₜ)ᵗ",
        "trap": "Discounting all cash flows with YTM."
    },
    {
        "id": "BENCHMARK_SPOT_RATES",
        "question": "You want rates derived from the benchmark yield curve.",
        "formula": "z₁, z₂, ..., zₙ",
        "trap": "Assuming spot rates equal YTM."
    },
    {
        "id": "Z_SPREAD",
        "question": "You want the constant spread added to all spot rates to match bond price.",
        "formula": "Z-spread per period",
        "trap": "Confusing it with OAS."
    },
    
    # --------------------------------
    # FORWARD RATES
    # --------------------------------
    
    {
        "id": "FORWARD_RATE_2Y_1Y",
        "question": "You want the one-year forward rate one year from now.",
        "formula": "(1+z₂)² / (1+z₁) − 1",
        "trap": "Using arithmetic instead of geometric relationship."
    },
    {
        "id": "FORWARD_RATES_INTERPRETATION",
        "question": "You want future implied short-term rates from spot rates.",
        "formula": "Geometric mean of forward rates equals spot rate",
        "trap": "Assuming forward rates are forecasts."
    },
    
    # --------------------------------
    # YIELD SPREADS
    # --------------------------------
    
    {
        "id": "YIELD_SPREAD",
        "question": "You want compensation over a benchmark yield.",
        "formula": "Bond YTM − Benchmark YTM",
        "trap": "Ignoring differences in maturity or credit quality."
    },
    {
        "id": "OAS",
        "question": "You want the spread excluding embedded option value.",
        "formula": "Option-Adjusted Spread",
        "trap": "Using Z-spread for callable bonds."
    },
    
    # --------------------------------
    # RISK PREMIUM DECOMPOSITION
    # --------------------------------
    
    {
        "id": "YTM_COMPONENTS",
        "question": "You want to decompose nominal interest rate.",
        "formula": "Nominal RF + Inflation + Credit + Liquidity + Tax",
        "trap": "Assuming all bonds share the same premiums."
    },
    {
        "id": "REAL_RATE",
        "question": "You want the return adjusted for expected inflation.",
        "formula": "Nominal Rate − Expected Inflation",
        "trap": "Using actual inflation instead of expected."
    },
    
    # --------------------------------
    # DURATION MEASURES
    # --------------------------------
    
    {
        "id": "MACAULAY_DURATION",
        "question": "You want the weighted average time to receive bond cash flows.",
        "formula": "Σ (PV(CFₜ) / Bond Price) × t",
        "trap": "Forgetting to weight by present value."
    },
    {
        "id": "MODIFIED_DURATION",
        "question": "You want price sensitivity to yield changes.",
        "formula": "MacDur / (1 + YTM)",
        "trap": "Using Macaulay duration directly."
    },
    {
        "id": "EFFECTIVE_DURATION",
        "question": "You want duration for bonds with embedded options.",
        "formula": "(V₋ − V₊) / (2·V₀·Δy)",
        "trap": "Using modified duration for callable bonds."
    },
    
    # --------------------------------
    # MONEY DURATION
    # --------------------------------
    
    {
        "id": "MONEY_DURATION",
        "question": "You want the dollar price change for a 1% change in yield.",
        "formula": "Modified Duration × Full Price",
        "trap": "Ignoring bond price level."
    },
    {
        "id": "PRICE_VALUE_BP",
        "question": "You want the price change for a 1 basis point change in yield.",
        "formula": "Money Duration / 10,000",
        "trap": "Using percentage instead of basis points."
    },
    
    # --------------------------------
    # FLOATING-RATE BONDS
    # --------------------------------
    
    {
        "id": "FRN_DURATION",
        "question": "You want the duration of a floating-rate note.",
        "formula": "Time to next reset",
        "trap": "Assuming long duration like fixed-rate bonds."
    }
    





]

TIMER_SECONDS = 15

# -------------------------------------------------
# SESSION STATE INIT
# -------------------------------------------------

if "question" not in st.session_state:
    st.session_state.question = random.choice(FORMULAS)
    st.session_state.start_time = time.time()
    st.session_state.show_options = False
    st.session_state.answered = False
    st.session_state.options = random.sample(FORMULAS, k=4)
    if st.session_state.question not in st.session_state.options:
        st.session_state.options[random.randint(0, 3)] = st.session_state.question

# -------------------------------------------------
# UI
# -------------------------------------------------

st.title("⏱️ CFA Level I – Formula Recognition Trainer")
st.markdown("**Think first. Formula appears after 15 seconds.**")

st.divider()

st.subheader("📌 Question")
st.write(st.session_state.question["question"])

# -------------------------------------------------
# TIMER
# -------------------------------------------------

elapsed = int(time.time() - st.session_state.start_time)
remaining = TIMER_SECONDS - elapsed

if remaining > 0:
    st.info(f"⏳ Think... {remaining} seconds")
    time.sleep(1)
    st.rerun()
else:
    st.session_state.show_options = True

# -------------------------------------------------
# OPTIONS (AFTER TIMER)
# -------------------------------------------------

if st.session_state.show_options and not st.session_state.answered:
    choice = st.radio(
        "Which formula applies?",
        st.session_state.options,
        format_func=lambda x: x["formula"]
    )

    if st.button("Check"):
        st.session_state.answered = True
        st.session_state.choice = choice

# -------------------------------------------------
# FEEDBACK
# -------------------------------------------------

if st.session_state.answered:
    correct = st.session_state.question

    if st.session_state.choice["id"] == correct["id"]:
        st.success("✅ Correct identification.")
    else:
        st.error("❌ Incorrect.")
        st.markdown(f"**Correct formula:** `{correct['formula']}`")
        st.warning(f"⚠️ Common trap: {correct['trap']}")

    if st.button("Next question"):
        st.session_state.question = random.choice(FORMULAS)
        st.session_state.start_time = time.time()
        st.session_state.show_options = False
        st.session_state.answered = False
        st.session_state.options = random.sample(FORMULAS, k=4)
        if st.session_state.question not in st.session_state.options:
            st.session_state.options[random.randint(0, 3)] = st.session_state.question
        st.rerun()
