import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Parameters ---
face_value = 100
coupon_rate = 0.05
recovery_rate = 0.4
risk_free_rate = 0.03
hazard_rate = 0.15
years = 5
frequency = 2

# --- Time Setup ---
dt = 1 / frequency
time_steps = np.arange(dt, years + dt, dt)

# --- Formula 1: Flow-Oriented with Debug Option ---
def npv_formula_1(face_value, coupon_rate, risk_free_rate, hazard_rate, recovery_rate, time_steps, debug=False):
    npv = 0
    coupon = face_value * coupon_rate / frequency
    data = []

    for t in time_steps:
        surv = np.exp(-hazard_rate * t)
        surv_prev = np.exp(-hazard_rate * (t - dt))
        default_prob = surv_prev - surv
        discount = np.exp(-risk_free_rate * t)
        coupon_leg = coupon * surv * discount
        recovery_leg = recovery_rate * face_value * default_prob * discount
        npv += coupon_leg + recovery_leg

        if debug:
            data.append({
                'Time (t)': round(t, 3),
                'Survival Prob': round(surv, 6),
                'Default Prob': round(default_prob, 6),
                'Discount Factor': round(discount, 6),
                'Coupon Leg': round(coupon_leg, 6),
                'Recovery Leg': round(recovery_leg, 6),
                'Cumulative NPV': round(npv, 6)
            })

    # Final Principal Repayment
    final_surv = np.exp(-hazard_rate * time_steps[-1])
    final_discount = np.exp(-risk_free_rate * time_steps[-1])
    final_leg = face_value * final_surv * final_discount
    npv += final_leg

    if debug:
        data.append({
            'Time (t)': round(time_steps[-1], 3),
            'Survival Prob': round(final_surv, 6),
            'Default Prob': 0.0,
            'Discount Factor': round(final_discount, 6),
            'Coupon Leg': 0.0,
            'Recovery Leg': 0.0,
            'Cumulative NPV': round(npv, 6)
        })
        return npv, pd.DataFrame(data)

    return npv

# --- Formula 2: Academic Notation with Debug Option ---
def npv_formula_2(face_value, coupon_rate, risk_free_rate, hazard_rate, recovery_rate, time_steps, debug=False):
    Q = lambda t: np.exp(-hazard_rate * t)
    Z = lambda t: np.exp(-risk_free_rate * t)
    C = face_value * coupon_rate
    f = frequency
    npv = 0
    data = []

    for i, t in enumerate(time_steps):
        Q_t = Q(t)
        Q_prev = Q(t - dt) if i > 0 else 1.0
        D_t = Q_prev - Q_t
        Z_t = Z(t)
        coupon_leg = Q_t * Z_t * (C / f)
        recovery_leg = D_t * Z_t * recovery_rate * face_value
        npv += coupon_leg + recovery_leg

        if debug:
            data.append({
                'Time (t)': round(t, 3),
                'Survival Prob': round(Q_t, 6),
                'Default Prob': round(D_t, 6),
                'Discount Factor': round(Z_t, 6),
                'Coupon Leg': round(coupon_leg, 6),
                'Recovery Leg': round(recovery_leg, 6),
                'Cumulative NPV': round(npv, 6)
            })

    final_Q = Q(time_steps[-1])
    final_Z = Z(time_steps[-1])
    final_leg = final_Q * final_Z * face_value
    npv += final_leg

    if debug:
        data.append({
            'Time (t)': round(time_steps[-1], 3),
            'Survival Prob': round(final_Q, 6),
            'Default Prob': 0.0,
            'Discount Factor': round(final_Z, 6),
            'Coupon Leg': 0.0,
            'Recovery Leg': 0.0,
            'Cumulative NPV': round(npv, 6)
        })
        return npv, pd.DataFrame(data)

    return npv

# --- Plotting Function ---
def plot_npv_components(df, title):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time (t)'], df['Coupon Leg'], label='Coupon Leg', marker='o')
    plt.plot(df['Time (t)'], df['Recovery Leg'], label='Recovery Leg', marker='s')
    plt.plot(df['Time (t)'], df['Cumulative NPV'], label='Cumulative NPV', linestyle='--', marker='x')
    plt.title(title)
    plt.xlabel("Time (Years)")
    plt.ylabel("Value ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- Run and Display ---
def main():
    npv1, df1 = npv_formula_1(face_value, coupon_rate, risk_free_rate, hazard_rate, recovery_rate, time_steps, debug=True)
    npv2, df2 = npv_formula_2(face_value, coupon_rate, risk_free_rate, hazard_rate, recovery_rate, time_steps, debug=True)

    # Print comparison
    print("\n📊 NPV Comparison\n")
    print(pd.DataFrame({
        'Formula': ['Flow-Oriented (Formula 1)', 'Academic Notation (Formula 2)'],
        'NPV ($)': [round(npv1, 6), round(npv2, 6)]
    }).to_string(index=False))

    # Print and plot Formula 1
    print("\n🔍 Detailed Formula 1 (Flow-Oriented)\n")
    print(df1.to_string(index=False))
    plot_npv_components(df1, "NPV Breakdown Over Time – Formula 1 (Flow-Oriented)")

    # Print and plot Formula 2
    print("\n🔍 Detailed Formula 2 (Academic Notation)\n")
    print(df2.to_string(index=False))
    plot_npv_components(df2, "NPV Breakdown Over Time – Formula 2 (Academic Notation)")

if __name__ == "__main__":
    main()
