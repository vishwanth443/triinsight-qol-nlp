# app/plot_full_mental_health_membership.py

import numpy as np
import matplotlib.pyplot as plt


MENTAL_HEALTH_TERMS = [
    "Burnout",
    "Overwhelmed",
    "Distressed",
    "Struggling",
    "Stressed",
    "Low",
    "Tense",
    "Stable",
    "Balanced",
    "Calm",
    "Relaxed",
    "Positive",
    "Peaceful",
    "Flourishing",
]

# Change this to: "triangular", "trapezoidal", or "gaussian"
SHAPE_TYPE = "trapezoidal"


def trimf(x, a, b, c):
    y = np.zeros_like(x, dtype=float)

    left = (x >= a) & (x <= b)
    right = (x >= b) & (x <= c)

    if b != a:
        y[left] = (x[left] - a) / (b - a)
    if c != b:
        y[right] = (c - x[right]) / (c - b)

    y[x == b] = 1.0
    return np.clip(y, 0, 1)


def trapmf(x, a, b, c, d):
    y = np.zeros_like(x, dtype=float)

    rise = (x >= a) & (x < b)
    top = (x >= b) & (x <= c)
    fall = (x > c) & (x <= d)

    if b != a:
        y[rise] = (x[rise] - a) / (b - a)
    y[top] = 1.0
    if d != c:
        y[fall] = (d - x[fall]) / (d - c)

    return np.clip(y, 0, 1)


def gaussmf(x, c, sigma):
    return np.exp(-0.5 * ((x - c) / sigma) ** 2)


def build_memberships(shape_type="gaussian"):
    x = np.linspace(0, 1, 2000)
    centers = np.linspace(1.0, 0.0, len(MENTAL_HEALTH_TERMS))
    step = centers[0] - centers[1]

    memberships = {}

    for i, term in enumerate(MENTAL_HEALTH_TERMS):
        center = centers[i]

        if shape_type == "triangular":
            if i == 0:
                a, b, c = center, center, center - step
            elif i == len(MENTAL_HEALTH_TERMS) - 1:
                a, b, c = center + step, center, center
            else:
                a, b, c = center + step, center, center - step

            memberships[term] = trimf(x, min(a, b, c), b, max(a, b, c))

        elif shape_type == "trapezoidal":
            if i == 0:
                a = center
                b = center
                c = center - step * 0.4
                d = center - step * 1.2
            elif i == len(MENTAL_HEALTH_TERMS) - 1:
                a = center + step * 1.2
                b = center + step * 0.4
                c = center
                d = center
            else:
                a = center + step * 1.2
                b = center + step * 0.4
                c = center - step * 0.4
                d = center - step * 1.2

            vals = sorted([a, b, c, d])
            memberships[term] = trapmf(x, vals[0], vals[1], vals[2], vals[3])

        elif shape_type == "gaussian":
            sigma = step * 0.45
            memberships[term] = gaussmf(x, center, sigma)

        else:
            raise ValueError("shape_type must be 'triangular', 'trapezoidal', or 'gaussian'")

    return x, memberships


def plot_full_mental_health_membership(shape_type="gaussian"):
    x, memberships = build_memberships(shape_type)

    plt.figure(figsize=(15, 8))
    colors = plt.cm.tab20(np.linspace(0, 1, len(MENTAL_HEALTH_TERMS)))

    for i, term in enumerate(MENTAL_HEALTH_TERMS):
        plt.plot(
            x,
            memberships[term],
            linewidth=2,
            color=colors[i],
            label=term
        )

    plt.title(f"Full Mental Health Membership Functions ({shape_type.title()})", fontsize=15, weight="bold")
    plt.xlabel("Mental Health severity universe", fontsize=12)
    plt.ylabel("Degree of membership", fontsize=12)
    plt.xlim(0, 1)
    plt.ylim(-0.02, 1.05)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_full_mental_health_membership(SHAPE_TYPE)