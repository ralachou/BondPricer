import numpy as np
import pandas as pd

# Shared parameters
face_value = 100
coupon_rate = 0.05
risk_free_rate = 0.03
recovery_rate = 0.4
years = 5
frequency = 2
dt = 1 / frequency
time_steps = np.arange(dt, years + dt, dt)

def survival_based_npv(face_value, coupon_rate, risk_free_rate, hazard_rate, recovery_rate, time_steps):
    npv = 0
    coupon = face_value * coupon_rate / frequency
    for t in time_steps:
        surv = np.exp(-hazard_rate * t)
        surv_prev = np.exp(-hazard_rate * (t - dt))
        default_prob = surv_prev - surv
        discount = np.exp(-risk_free_rate * t)

        npv += coupon * surv * discount
        npv += recovery_rate * face_value * default_prob * discount

    final_surv = np.exp(-hazard_rate * time_steps[-1])
    final_discount = np.exp(-risk_free_rate * time_steps[-1])
    final_leg = face_value * final_surv * final_discount
    npv += final_leg
    return npv

# --- Case Definitions ---
# Case 1: Bond becomes distressed halfway (B → CCC)
def simulate_case_1():
    hazard_B = 0.05
    hazard_CCC = 0.30
    mid_index = int(len(time_steps) / 2)
    npv = 0
    coupon = face_value * coupon_rate / frequency
    for i, t in enumerate(time_steps):
        hazard = hazard_B if i < mid_index else hazard_CCC
        surv = np.exp(-hazard * t)
        surv_prev = np.exp(-hazard * (t - dt))
        default_prob = surv_prev - surv
        discount = np.exp(-risk_free_rate * t)
        npv += coupon * surv * discount
        npv += recovery_rate * face_value * default_prob * discount
    final_surv = np.exp(-hazard_CCC * time_steps[-1])
    final_discount = np.exp(-risk_free_rate * time_steps[-1])
    npv += face_value * final_surv * final_discount
    return npv

# Case 2: Distressed from the start but still accrues
def simulate_case_2():
    hazard = 0.35
    return survival_based_npv(face_value, coupon_rate, risk_free_rate, hazard, recovery_rate, time_steps)

# Case 3: Market price dropped significantly (observe implied NPV, not modeled directly here)
def simulate_case_3():
    # Just assume price dropped, simulate high hazard
    hazard = 0.45
    return survival_based_npv(face_value, coupon_rate, risk_free_rate, hazard, recovery_rate, time_steps)

# Case 4: Defaulted already (no future flows)
def simulate_case_4():
    # Assume only recovery applies now, no coupons
    return recovery_rate * face_value

def simulate_case_0():
    hazard = 0.02  # A-rated bond
    return survival_based_npv(face_value, coupon_rate, risk_free_rate, hazard, recovery_rate, time_steps)


def simulate_case_5():
    # Assume no coupons are paid — only recovery applied over a staggered default timeline
    hazard = 0.35
    npv = 0
    for t in time_steps:
        surv = np.exp(-hazard * t)
        surv_prev = np.exp(-hazard * (t - dt))
        default_prob = surv_prev - surv
        discount = np.exp(-risk_free_rate * t)
        # Only recovery leg (no coupons)
        npv += recovery_rate * face_value * default_prob * discount
    # No principal added since it's not paid
    return npv

# Run all cases
npv_0 = simulate_case_0()
npv_1 = simulate_case_1()
npv_2 = simulate_case_2()
npv_3 = simulate_case_3()
npv_4 = simulate_case_4()
npv_5 = simulate_case_5()

# Update DataFrame
df_cases = pd.DataFrame({
    'Scenario': [
        "Case 0: Investment Grade (A rating)",
        "Case 1: Downgraded midlife (B → CCC)",
        "Case 2: Already distressed but accruing",
        "Case 3: Price dropped significantly",
        "Case 4: Defaulted (recovery only)",
        "Case 5: Distressed, no more interest"
    ],
    'NPV ($)': [round(npv_0, 6), round(npv_1, 6), round(npv_2, 6), round(npv_3, 6), round(npv_4, 6), round(npv_5, 6)]
})


# Display updated table
print("\n📊 Updated NPV Scenarios (Including Case 5: No More Accrual)\n")
print(df_cases.to_string(index=False))





