import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ace_tools as tools

# Simulation Parameters
years = 10  # Simulate over 10 years
initial_par = 1000  # Par value of bond
coupon_rate = 0.05  # Initial coupon rate (5%)
spread = 0.50  # Fixed spread in % 
discount_rate = 0.04  # Market discount rate for pricing

# Generate a time series for each type of schedule
years_range = np.arange(1, years + 1)

# 1. Call Schedule (Issuer can redeem early at declining prices)
call_prices = [105, 103, 101, 100] + [100] * (years - 4)  # Declining call prices

# 2. Put Schedule (Investor can redeem early at fixed prices)
put_prices = [100] * years  # Investors can sell at par

# 3. Sinking Fund Schedule (Partial repayments each year)
sinking_fund = np.linspace(initial_par, 0, years)  # Linear decrease in principal

# 4. Multi-Step Coupon Schedule (Rate changes over time)
multi_step_coupons = [3, 4, 5, 6, 6, 7, 7, 7, 8, 8]  # Step-up coupon rate

# 5. Amortized Bond Schedule (Principal paid gradually)
amortized_principal = np.linspace(initial_par, 0, years)  # Gradual principal reduction
amortized_interest = (amortized_principal[:-1] + amortized_principal[1:]) / 2 * coupon_rate
amortized_payment = amortized_interest + np.diff(amortized_principal)

# 6. Pre-Refunded Bond (Paid off early)
pre_refunded_year = 5  # Pre-refunded after 5 years
pre_refunded_price = 102  # Bond refunded at 102% of par
pre_refund_schedule = [pre_refunded_price if yr == pre_refunded_year else np.nan for yr in years_range]

# Create DataFrame
df = pd.DataFrame({
    "Year": years_range,
    "Call Price (%)": call_prices,
    "Put Price (%)": put_prices,
    "Sinking Fund Balance": sinking_fund,
    "Multi-Step Coupon (%)": multi_step_coupons,
    "Amortized Principal": np.append(amortized_principal[:-1], 0),  # Ensuring size consistency
    "Amortized Interest Payment": np.append(amortized_interest, 0),  # Filling last missing value with zero
    "Amortized Total Payment": np.append(amortized_payment, 0),  # Filling last missing value with zero
    "Pre-Refunded Price": pre_refund_schedule
})

# Display DataFrame
tools.display_dataframe_to_user(name="Bond Features Simulation", dataframe=df)

# Plot Call vs. Put Schedule
plt.figure(figsize=(12, 6))
plt.plot(df["Year"], df["Call Price (%)"], label="Call Price", marker='o', linestyle='dashed')
plt.plot(df["Year"], df["Put Price (%)"], label="Put Price", marker='o', linestyle='dotted')
plt.xlabel("Year")
plt.ylabel("Price (% of Par)")
plt.title("Call vs. Put Schedule")
plt.legend()
plt.grid(True)
plt.show()

# Plot Sinking Fund Balance
plt.figure(figsize=(12, 6))
plt.plot(df["Year"], df["Sinking Fund Balance"], label="Sinking Fund Balance", linewidth=2, color='purple')
plt.xlabel("Year")
plt.ylabel("Remaining Principal")
plt.title("Sinking Fund Schedule")
plt.legend()
plt.grid(True)
plt.show()

# Plot Multi-Step Coupon Schedule
plt.figure(figsize=(12, 6))
plt.plot(df["Year"], df["Multi-Step Coupon (%)"], label="Multi-Step Coupon Rate", marker='s', linewidth=2, color='orange')
plt.xlabel("Year")
plt.ylabel("Coupon Rate (%)")
plt.title("Multi-Step Bond Coupon Schedule")
plt.legend()
plt.grid(True)
plt.show()

# Plot Amortized Principal & Payments
plt.figure(figsize=(12, 6))
plt.plot(df["Year"], df["Amortized Principal"], label="Amortized Principal", linewidth=2, color='blue')
plt.plot(df["Year"], df["Amortized Total Payment"], label="Total Payment (Interest + Principal)", linestyle='dashed', color='red')
plt.xlabel("Year")
plt.ylabel("Amount")
plt.title("Amortized Bond Payment Schedule")
plt.legend()
plt.grid(True)
plt.show()

# Plot Pre-Refunded Bond Schedule
plt.figure(figsize=(12, 6))
plt.plot(df["Year"], df["Pre-Refunded Price"], label="Pre-Refunded Price", marker='D', linestyle='dotted', color='green')
plt.xlabel("Year")
plt.ylabel("Price (% of Par)")
plt.title("Pre-Refunded Bond Redemption Schedule")
plt.legend()
plt.grid(True)
plt.show()
