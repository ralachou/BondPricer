import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --- Model Definitions (Same as before) ---

def survival_based_pricing(face_value, coupon_rate, years, risk_free_rate, hazard_rate, recovery_rate, frequency=2):
    dt = 1 / frequency
    periods = int(years * frequency)
    coupon = face_value * coupon_rate / frequency
    npv = 0
    for i in range(1, periods + 1):
        t = i * dt
        survival_prob = np.exp(-hazard_rate * t)
        default_prob = np.exp(-hazard_rate * (t - dt)) - survival_prob
        discount_factor = np.exp(-risk_free_rate * t)
        npv += coupon * survival_prob * discount_factor
        npv += recovery_rate * face_value * default_prob * discount_factor
    npv += face_value * survival_prob * np.exp(-risk_free_rate * years)
    return npv


def oas_model(face_value, coupon_rate, years, oas_spread, call_price, call_year,
              r0=0.03, sigma=0.01, frequency=2, n_paths=200):
    dt = 1 / frequency
    n_steps = int(years * frequency)
    rates = np.zeros((n_paths, n_steps + 1))
    rates[:, 0] = r0
    for t in range(1, n_steps + 1):
        dW = np.random.normal(0, np.sqrt(dt), size=n_paths)
        rates[:, t] = rates[:, t - 1] * np.exp(-0.5 * sigma ** 2 * dt + sigma * dW)
    prices = []
    for path in rates:
        price = 0
        called = False
        for i in range(1, n_steps + 1):
            t = i * dt
            df = np.exp(-np.sum(path[:i]) * dt - oas_spread * t)
            cash_flow = face_value * coupon_rate / frequency
            if i == n_steps:
                cash_flow += face_value
            if call_year and t >= call_year and not called:
                if df * call_price < call_price:
                    price += call_price * df
                    called = True
                    break
            price += cash_flow * df
        prices.append(price)
    return np.mean(prices)


def rating_based_pricing(face_value, coupon_rate, years, rating_defaults, recovery_rate, risk_free_rate, frequency=1):
    npv = 0
    coupon = face_value * coupon_rate / frequency
    for i, pd in enumerate(rating_defaults[:int(years)]):
        t = i + 1
        survival_prob = 1 - sum(rating_defaults[:t])
        default_prob = pd
        df = np.exp(-risk_free_rate * t)
        npv += coupon * survival_prob * df
        npv += recovery_rate * face_value * default_prob * df
    final_survival = 1 - sum(rating_defaults[:int(years)])
    npv += face_value * final_survival * np.exp(-risk_free_rate * years)
    return npv


# --- Plotting Functions ---

def plot_recovery_sensitivity(df_recovery):
    plt.figure(figsize=(8, 5))
    plt.plot(df_recovery['Recovery Rate'], df_recovery['NPV (Survival-Based)'], marker='o', label='Survival-Based')
    plt.plot(df_recovery['Recovery Rate'], df_recovery['NPV (Rating-Based)'], marker='s', label='Rating-Based')
    plt.title("NPV Sensitivity to Recovery Rate")
    plt.xlabel("Recovery Rate")
    plt.ylabel("NPV ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_hazard_vs_npv(df_hazard):
    plt.figure(figsize=(8, 5))
    plt.plot(df_hazard['Hazard Rate'], df_hazard['NPV (Survival-Based)'], marker='o', color='tomato')
    plt.title("NPV vs Hazard Rate (Survival-Based Pricing)")
    plt.xlabel("Hazard Rate")
    plt.ylabel("NPV ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_oas_vs_npv(df_oas):
    plt.figure(figsize=(8, 5))
    plt.plot(df_oas['OAS Spread (bps)'], df_oas['NPV (Callable Bond)'], marker='x', color='slateblue')
    plt.title("NPV vs OAS Spread (Callable Bond)")
    plt.xlabel("OAS Spread (bps)")
    plt.ylabel("NPV ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# --- Main Execution ---

def main():
    face_value = 100
    coupon_rate = 0.05
    years = 5
    risk_free_rate = 0.03
    call_price = 100
    call_year = 3

    recovery_rates = np.linspace(0.1, 0.9, 9)
    rating_defaults = [0.02, 0.025, 0.03, 0.035, 0.04]
    df_recovery = pd.DataFrame({
        'Recovery Rate': recovery_rates,
        'NPV (Survival-Based)': [survival_based_pricing(face_value, coupon_rate, years, risk_free_rate, 0.15, r) for r
                                 in recovery_rates],
        'NPV (Rating-Based)': [rating_based_pricing(face_value, coupon_rate, years, rating_defaults, r, risk_free_rate)
                               for r in recovery_rates]
    })

    hazard_rates = np.linspace(0.01, 0.30, 30)
    df_hazard = pd.DataFrame({
        'Hazard Rate': hazard_rates,
        'NPV (Survival-Based)': [survival_based_pricing(face_value, coupon_rate, years, risk_free_rate, h, 0.4) for h in
                                 hazard_rates]
    })

    oas_values = np.linspace(0.0, 0.1, 20)
    df_oas = pd.DataFrame({
        'OAS Spread (bps)': oas_values * 10000,
        'NPV (Callable Bond)': [oas_model(face_value, coupon_rate, years, oas, call_price, call_year) for oas in
                                oas_values]
    })

    # Print DataFrames locally
    print("\n📊 Recovery Rate Sensitivity\n")
    print(df_recovery.to_string(index=False))

    print("\n📊 Hazard Rate Sensitivity\n")
    print(df_hazard.to_string(index=False))

    print("\n📊 OAS Spread Sensitivity\n")
    print(df_oas.to_string(index=False))

    # Plot all sensitivity charts
    plot_recovery_sensitivity(df_recovery)
    plot_hazard_vs_npv(df_hazard)
    plot_oas_vs_npv(df_oas)


if __name__ == "__main__":
    main()
