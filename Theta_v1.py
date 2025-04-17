import numpy as np
import pandas as pd

# Example setup: survival-based pricing of a distressed bond

# Bond parameters
face_value = 100  # par value
coupon_rate = 0.08  # 8% annual coupon
frequency = 2  # semi-annual
recovery_rate = 0.4  # 40% recovery on default
maturity_years = 5
valuation_date = 0

# Market and curve data
risk_free_rate = 0.03  # 3% flat risk-free rate
hazard_rate = 0.25  # constant hazard rate of 25% annually

# Time points
payment_times = np.arange(1 / frequency, maturity_years + 1 / frequency, 1 / frequency)


# Functions
def discount_factor(t, r=risk_free_rate):
    return np.exp(-r * t)


def survival_probability(t, h=hazard_rate):
    return np.exp(-h * t)


def default_probability(t1, t0, h=hazard_rate):
    return survival_probability(t0, h) - survival_probability(t1, h)


# Calculate price under survival-based model
def survival_based_bond_price():
    price = 0
    for t in payment_times:
        # Expected coupon and principal if no default
        cashflow = (face_value * coupon_rate / frequency)
        price += cashflow * discount_factor(t) * survival_probability(t)

    # Add expected principal repayment at maturity
    price += face_value * discount_factor(maturity_years) * survival_probability(maturity_years)

    # Add expected recovery value if default occurs between periods
    for t in payment_times:
        dp = default_probability(t, t - 1 / frequency)
        price += face_value * recovery_rate * discount_factor(t) * dp

    return price


# Calculate theta (1-day passage of time)
def calculate_theta():
    price_today = survival_based_bond_price()

    # Move forward 1 day
    dt = 1 / 252  # 1 trading day
    new_times = payment_times - dt
    new_times = new_times[new_times > 0]

    theta_price = 0
    for t in new_times:
        cashflow = (face_value * coupon_rate / frequency)
        theta_price += cashflow * discount_factor(t) * survival_probability(t)
    theta_price += face_value * discount_factor(maturity_years - dt) * survival_probability(maturity_years - dt)

    for t in new_times:
        t0 = t - 1 / frequency
        if t0 < 0: t0 = 0
        dp = default_probability(t, t0)
        theta_price += face_value * recovery_rate * discount_factor(t) * dp

    theta = theta_price - price_today
    return price_today, theta_price, theta


# Run the calculation
price_today, price_tomorrow, theta = calculate_theta()

import ace_tools as tools;

tools.display_dataframe_to_user(name="Bond Theta Example", dataframe=pd.DataFrame({
    'Metric': ['Price Today', 'Price Tomorrow (1-day later)', 'Theta (PnL from Time Passage)'],
    'Value': [price_today, price_tomorrow, theta]
}))
