# fuzzy_plot.py

import numpy as np
import matplotlib.pyplot as plt


def mu_low(k: float) -> float:
    if k <= 0:
        return 1.0
    elif 0 < k < 2:
        return max(0.0, (2 - k) / 2.0)
    else:
        return 0.0


def mu_medium(k: float) -> float:
    if k <= 0 or k >= 4:
        return 0.0
    elif 0 < k <= 2:
        return k / 2.0
    else:  # 2 < k < 4
        return max(0.0, (4 - k) / 2.0)


def mu_high(k: float) -> float:
    if k <= 2:
        return 0.0
    elif 2 < k < 4:
        return (k - 2) / 2.0
    else:  # k >= 4
        return 1.0


def print_membership_table():
    print("k\tmu_low\tmu_medium\tmu_high")
    for k in range(0, 7):
        l = mu_low(k)
        m = mu_medium(k)
        h = mu_high(k)
        print(f"{k}\t{l:.2f}\t{m:.2f}\t\t{h:.2f}")


def plot_fuzzy_sets():
    ks = np.linspace(0, 6, 601)  # 0.01 step

    mu_l = [mu_low(x) for x in ks]
    mu_m = [mu_medium(x) for x in ks]
    mu_h = [mu_high(x) for x in ks]

    plt.figure(figsize=(8, 5))
    plt.plot(ks, mu_l, label="Low", color="blue")
    plt.plot(ks, mu_m, label="Medium", color="orange")
    plt.plot(ks, mu_h, label="High", color="red")

    plt.title("Fuzzy Membership Functions for BOW Score k")
    plt.xlabel("k (BOW score / keyword count)")
    plt.ylabel("Membership degree")
    plt.ylim(-0.05, 1.05)
    plt.xlim(0, 6)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Fuzzy membership table (values printed in command prompt):")
    print_membership_table()

    print("\nOpening fuzzy set plot window...")
    plot_fuzzy_sets()