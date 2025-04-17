import numpy as np
import pandas as pd

# Define the valuation function for a zero-coupon bond
def valuation_zero_coupon_bond(notional, rate, ttm, convention='annual'):
    """
    Valuation of a zero-coupon bond using simple compounding.

    Args:
        notional (float): Face value of the bond.
        rate (float): Annualized interest rate.
        ttm (float): Time to maturity in years.
        convention (str): Compounding convention ('annual', 'semi-annual', 'continuous').

    Returns:
        float: Present value of the zero-coupon bond.
    """
    if convention == 'annual':
        return notional / (1 + rate) ** ttm
    elif convention == 'semi-annual':
        return notional / (1 + rate / 2) ** (2 * ttm)
    elif convention == 'continuous':
        return notional * np.exp(-rate * ttm)
    else:
        raise ValueError("Unsupported compounding convention.")

# Example from the document
notional = 100  # Face value
rate = 0.04     # 4% interest
convention = 'annual'

# TMP decomposition valuations
V1 = valuation_zero_coupon_bond(notional, rate, 1.0, convention)      # Yesterday: 1 year to maturity
V2 = valuation_zero_coupon_bond(notional, rate, 0.997, convention)    # Today: 1 day forward
V3 = valuation_zero_coupon_bond(notional, 0.06, 0.997, convention)    # Market shift: 6% rate
V4 = V3                                                               # No position change (same zero coupon bond)

cash_flows = 0  # Zero coupon bonds do not pay interim cash flows

# Compute PnL components
theta = V2 - V1
hypo_pnl = V3 - V2
position_pnl = V4 - V3 + cash_flows
comprehensive_pnl = V4 - V1 + cash_flows

# Display
df = pd.DataFrame({
    'PnL Component': ['Theta (Time)', 'Hypothetical PnL (Market)', 'Position PnL (Activity)', 'Comprehensive PnL'],
    'Value': [theta, hypo_pnl, position_pnl, comprehensive_pnl]
})

import ace_tools as tools
tools.display_dataframe_to_user(name="Zero Coupon Bond PnL Attribution", dataframe=df)
