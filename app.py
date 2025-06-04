import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Center the logo using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("PRM Logo.png", width=700)

st.markdown("""
This tool helps you simulate how your business profit and cash flow respond to unexpected shocks such as demand drops, cost increases, or delayed payments.  
            
Enter your variables to evaluate your business resilience!
""")

company_presets = {
    "Custom": {
        "revenue": 120_000,
        "fixed_costs": 45_000,
        "variable_costs": 30_000,
        "initial_cash": 10_000
    },
    "Alphabet (Google)": {
        "revenue": 307_000_000_000,
        "fixed_costs": 50_000_000_000,
        "variable_costs": 150_000_000_000,
        "initial_cash": 108_000_000_000
    },
    "Amazon": {
        "revenue": 575_000_000_000,
        "fixed_costs": 40_000_000_000,
        "variable_costs": 480_000_000_000,
        "initial_cash": 73_000_000_000
    },
    "Apple": {
        "revenue": 383_000_000_000,
        "fixed_costs": 32_000_000_000,
        "variable_costs": 245_000_000_000,
        "initial_cash": 74_000_000_000
    },
    "Meta (Facebook)": {
        "revenue": 135_000_000_000,
        "fixed_costs": 30_000_000_000,
        "variable_costs": 55_000_000_000,
        "initial_cash": 58_000_000_000
    },
    "Microsoft": {
        "revenue": 212_000_000_000,
        "fixed_costs": 30_000_000_000,
        "variable_costs": 110_000_000_000,
        "initial_cash": 81_000_000_000
    },
    "Netflix": {
        "revenue": 34_000_000_000,
        "fixed_costs": 5_000_000_000,
        "variable_costs": 24_000_000_000,
        "initial_cash": 7_000_000_000
    },
    "Tesla": {
        "revenue": 97_000_000_000,
        "fixed_costs": 7_000_000_000,
        "variable_costs": 75_000_000_000,
        "initial_cash": 29_000_000_000
    }
}

company_choice = st.selectbox(
    "Select a company for their finances (or 'Custom' to enter your own):",
    list(company_presets.keys()),
    index=0
)

if "revenue" not in st.session_state:
    st.session_state["revenue"] = company_presets[company_choice]["revenue"]
    st.session_state["fixed_costs"] = company_presets[company_choice]["fixed_costs"]
    st.session_state["variable_costs"] = company_presets[company_choice]["variable_costs"]
    st.session_state["initial_cash"] = company_presets[company_choice]["initial_cash"]

if st.session_state.get("last_company", None) != company_choice:
    st.session_state["revenue"] = company_presets[company_choice]["revenue"]
    st.session_state["fixed_costs"] = company_presets[company_choice]["fixed_costs"]
    st.session_state["variable_costs"] = company_presets[company_choice]["variable_costs"]
    st.session_state["initial_cash"] = company_presets[company_choice]["initial_cash"]
    st.session_state["last_company"] = company_choice

# --- Baseline inputs, side by side ---
st.header("1. Baseline Scenario")

col1, col2, col3, col4 = st.columns(4)
with col1:
    revenue = st.number_input(
        "Annual Revenue (£)", min_value=0, value=st.session_state["revenue"], step=1_000_000
    )
with col2:
    fixed_costs = st.number_input(
        "Annual Fixed Costs (£)", min_value=0, value=st.session_state["fixed_costs"], step=1_000_000
    )
with col3:
    variable_costs = st.number_input(
        "Annual Variable Costs (£)", min_value=0, value=st.session_state["variable_costs"], step=1_000_000
    )
with col4:
    initial_cash = st.number_input(
        "Initial Cash (£)", min_value=0, value=st.session_state["initial_cash"], step=1_000_000
    )

st.markdown("---")

# --- Preset Scenarios ---
st.header("2. Stress Test: Select Market Shocks")

preset_options = {
    "No Shock (Default)": {
        "demand_drop": 0,
        "payment_delay_months": 0,
        "cost_increase": 0,
        "regulation_cost": 0,
    },
    "Competitor Innovation (Lower Prices)": {
        "demand_drop": 15,
        "payment_delay_months": 0,
        "cost_increase": 0,
        "regulation_cost": 0,
    },
    "Fuel Price Spike": {
        "demand_drop": 0,
        "payment_delay_months": 0,
        "cost_increase": 30,
        "regulation_cost": 0,
    },
    "Payment Delays Worsen": {
        "demand_drop": 0,
        "payment_delay_months": 3,
        "cost_increase": 0,
        "regulation_cost": 0,
    },
    "Sudden Regulation": {
        "demand_drop": 0,
        "payment_delay_months": 0,
        "cost_increase": 0,
        "regulation_cost": 8_000_000_000,
    }
}

preset = st.selectbox("Choose a preset scenario:", list(preset_options.keys()), index=0)

# Set or override default values using session_state so users can still manually adjust
if "demand_drop" not in st.session_state:
    st.session_state["demand_drop"] = preset_options[preset]["demand_drop"]
    st.session_state["payment_delay_months"] = preset_options[preset]["payment_delay_months"]
    st.session_state["cost_increase"] = preset_options[preset]["cost_increase"]
    st.session_state["regulation_cost"] = preset_options[preset]["regulation_cost"]

if st.session_state.get("last_preset", None) != preset:
    st.session_state["demand_drop"] = preset_options[preset]["demand_drop"]
    st.session_state["payment_delay_months"] = preset_options[preset]["payment_delay_months"]
    st.session_state["cost_increase"] = preset_options[preset]["cost_increase"]
    st.session_state["regulation_cost"] = preset_options[preset]["regulation_cost"]
    st.session_state["last_preset"] = preset

col5, col6 = st.columns(2)
with col5:
    demand_drop = st.slider("Demand Drop (%)", 0, 100, st.session_state["demand_drop"], step=5, key="demand_drop")
    payment_delay_months = st.slider("Payment Delay (Months)", 0, 6, st.session_state["payment_delay_months"], key="payment_delay_months")
with col6:
    cost_increase = st.slider("Variable Cost Increase (%)", 0, 100, st.session_state["cost_increase"], step=5, key="cost_increase")
    regulation_cost = st.number_input("One-off Regulatory Cost (£)", min_value=0, value=st.session_state["regulation_cost"], step=1_000_000, key="regulation_cost")

# --- Simulation Length ---
st.markdown("---")
st.header("3. Simulation Length")
sim_length = st.radio(
    "Select simulation period:",
    options=[12, 24, 48],
    format_func=lambda x: f"{x} months",
    index=0
)

# --- Scenario Simulation ---
st.header("4. Scenario Simulation Results")

# Baseline calculations
annual_profit = revenue - fixed_costs - variable_costs
baseline_cash = initial_cash + annual_profit

# Shock calculations
shock_revenue = revenue * (1 - demand_drop / 100)
shock_variable_costs = variable_costs * (1 + cost_increase / 100)
shock_profit = shock_revenue - fixed_costs - shock_variable_costs - regulation_cost

months = list(range(1, sim_length + 1))
baseline_cashflow = []
shock_cashflow = []

baseline_balance = initial_cash
shock_balance = initial_cash

for m in months:
    # Payments received in shock scenario are delayed
    if m <= payment_delay_months:
        shock_income = 0
    else:
        shock_income = shock_revenue / 12
    baseline_balance += (revenue / 12) - (fixed_costs / 12) - (variable_costs / 12)
    shock_balance += shock_income - (fixed_costs / 12) - (shock_variable_costs / 12)
    if m == 1:
        shock_balance -= regulation_cost  # apply one-off cost in month 1
    baseline_cashflow.append(baseline_balance)
    shock_cashflow.append(shock_balance)

# --- Visualization ---
df = pd.DataFrame({
    "Month": months,
    "Baseline scenario (£)": baseline_cashflow,
    "Shocked scenario (£)": shock_cashflow,
})

fig, ax = plt.subplots()
ax.plot(df["Month"], df["Baseline scenario (£)"], label="Baseline scenario", color='green')
ax.plot(df["Month"], df["Shocked scenario (£)"], label="Shocked scenario", color='red', linestyle="--")
ax.set_xlabel("Month")
ax.set_ylabel("Cash Balance (£)")
ax.set_title("Cash Flow Projection: Baseline vs Shock")
ax.legend()
st.pyplot(fig)

# --- Resilience Insights ---
st.subheader("Resilience Insights")

insights = []

if shock_profit < 0:
    insights.append("🔴 **Warning:** Your business is not profitable under the shocked scenario. Consider cost-saving measures or new revenue sources.")
else:
    profit_change = shock_profit - annual_profit
    if profit_change < 0:
        percent_drop = abs(profit_change) / (abs(annual_profit) + 1e-6) * 100
        if percent_drop < 10:
            insights.append("🟡 **Minor impact:** Profit declines slightly under shock, but business remains resilient.")
        elif percent_drop < 30:
            insights.append("🟠 **Moderate impact:** Significant drop in profit. Caution: monitor closely and explore mitigations.")
        else:
            insights.append("🔴 **Major impact:** Profit drops sharply. Review strategies for resilience.")
    else:
        insights.append("🟢 **No negative impact:** Your profit increases under this scenario.")

if min(shock_cashflow) < 0:
    negative_month = months[shock_cashflow.index(min(shock_cashflow))]
    insights.append(f"🔴 **Critical:** Cash runs out in month {negative_month} of the simulation. Immediate changes required to avoid insolvency.")
else:
    if shock_profit >= 0:
        insights.append("🟢 **Strong cash position:** Cash remains positive throughout the simulation under shock.")
    else:
        insights.append("🟡 **Cash positive but unprofitable:** You remain solvent for now, but review your profit model.")

for insight in insights:
    st.markdown(insight)

# --- Summary Table ---
st.subheader("Summary Table")
summary_table = pd.DataFrame({
    "Scenario": ["Baseline scenario", "Shocked scenario"],
    "Annual Profit (£)": [annual_profit, shock_profit],
    f"End-of-Simulation Cash (£) [{sim_length} mo]": [baseline_cashflow[-1], shock_cashflow[-1]]
})
st.write(summary_table)


st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write("Profit Resilience Model © ¦ Created by Tom Loosley ¦ Published in 2025")
st.markdown("Found a problem? <a href='mailto:loosleytom@gmail.com'>Report an issue</a>", unsafe_allow_html=True)
