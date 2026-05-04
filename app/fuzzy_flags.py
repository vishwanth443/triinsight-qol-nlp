# app/fuzzy_flags.py

from pathlib import Path

from app.bow_data import DOMAINS, compute_domain_bow_scores


def mu_low(k: int) -> float:
    if k <= 0:
        return 1.0
    elif 0 < k < 2:
        return max(0.0, (2 - k) / 2.0)
    else:
        return 0.0


def mu_medium(k: int) -> float:
    if k <= 0 or k >= 4:
        return 0.0
    elif 0 < k <= 2:
        return k / 2.0
    else:
        return max(0.0, (4 - k) / 2.0)


def mu_high(k: int) -> float:
    if k <= 2:
        return 0.0
    elif 2 < k < 4:
        return (k - 2) / 2.0
    else:
        return 1.0


def severity_from_k(k: int) -> float:
    low = mu_low(k)
    med = mu_medium(k)
    high = mu_high(k)

    num = 0.0 * low + 0.5 * med + 1.0 * high
    den = low + med + high

    if den == 0:
        return 0.0

    return num / den


def severity_to_flag(sev: float) -> str:
    if sev < 0.2:
        return "blue"
    elif sev < 0.4:
        return "green"
    elif sev < 0.6:
        return "amber"
    elif sev < 0.8:
        return "red"
    else:
        return "dark_red"


def analyse_patient_fuzzy(json_path: Path):
    patient_id, domain_texts, domain_scores, domain_vectors = compute_domain_bow_scores(
        json_path
    )

    results = {}
    for domain in DOMAINS:
        text = domain_texts[domain]
        bow_score = domain_scores[domain]
        sev = severity_from_k(bow_score)
        flag = severity_to_flag(sev)
        label = 1 if sev >= 0.4 else 0

        results[domain] = {
            "bow_score": bow_score,
            "severity": round(sev, 3),
            "flag": flag,
            "label": label,
            "text": text,
            "bow_vector": domain_vectors[domain],
        }

    return patient_id, results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m app.fuzzy_flags data/real/p001.json")
        raise SystemExit(1)

    json_path = Path(sys.argv[1])
    pid, results = analyse_patient_fuzzy(json_path)

    print(f"\nPatient: {pid} ({json_path.name})\n")
    for domain, info in results.items():
        print(
            f"[{domain}] flag={info['flag']} "
            f"severity={info['severity']:.3f} "
            f"bow_score={info['bow_score']} "
            f"label={info['label']}"
        )
        print(f" text: {info['text']}\n")