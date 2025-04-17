import numpy as np
import pandas as pd

# Define valuation function for zero-coupon bond
def valuation_zero_coupon_bond(notional, rate, ttm, convention='annual'):
    if convention == 'annual':
        return notional / (1 + rate) ** ttm
    elif convention == 'semi-annual':
        return notional / (1 + rate / 2) ** (2 * ttm)
    elif convention == 'continuous':
        return notional * np.exp(-rate * ttm)
    else:
        raise ValueError("Unsupported compounding convention.")

# Inputs
notional = 100
rate_t_minus_1 = 0.04      # Yesterday's market rate
rate_t = 0.06              # Today's market rate (market moved)
convention = 'annual'
ttm_t_minus_1 = 360 / 360  # 1 year
ttm_t = 359 / 360          # 1 day later

# Valuations
V1 = valuation_zero_coupon_bond(notional, rate_t_minus_1, ttm_t_minus_1, convention)  # Yesterday
V2 = valuation_zero_coupon_bond(notional, rate_t_minus_1, ttm_t, convention)          # Today, same market
V3 = valuation_zero_coupon_bond(notional, rate_t, ttm_t, convention)                  # Today, market moved
V4 = V3  # No new trade, so position unchanged
cash_flows = 0  # Zero coupon bond: no interim cash flows

# PnL components
theta = V2 - V1
hypo_pnl = V3 - V2
position_pnl = V4 - V3 + cash_flows
comprehensive_pnl = V4 - V1 + cash_flows

# Display
df = pd.DataFrame({
    'Component': ['Valuation T-1 (V1)', 'Theta Valuation (V2)', 'Market Valuation (V3)', 'Final Valuation (V4)',
                  'Theta (Time PnL)', 'Hypothetical PnL (Market)', 'Position PnL (Activity)', 'Comprehensive PnL'],
    'Value': [V1, V2, V3, V4, theta, hypo_pnl, position_pnl, comprehensive_pnl]
})

import ace_tools as tools
tools.display_dataframe_to_user(name="Zero Coupon Bond PnL Using TTM Logic", dataframe=df)
