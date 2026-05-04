# app/keyword_counts.py

from pathlib import Path
import json
from collections import Counter

from app.bow_data import load_patient, DOMAINS


def load_keywords(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def count_keywords(text: str, keywords: list[str]) -> int:
    text_l = text.lower()
    counts = 0
    for kw in keywords:
        if kw in text_l:
            counts += 1
    return counts


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m app.keyword_counts data/real/p001.json")
        raise SystemExit(1)

    json_path = Path(sys.argv[1])
    kw_path = Path("config/keywords.json")

    patient = load_patient(json_path)
    keywords = load_keywords(kw_path)

    q = patient["quality_of_life"]["free_text"]

    print(f"\nPatient: {patient.get('patient_id')} ({json_path.name})\n")

    # Per domain counts
    for domain in DOMAINS:
        text = q[domain]
        klist = keywords.get(domain, [])
        c = count_keywords(text, klist)
        print(f"[{domain}] keyword_hits={c}")
        print(f"  text: {text}\n")

    # Overall counts across all domains
    all_text = " ".join(q[d] for d in DOMAINS)
    overall = {}
    for domain in DOMAINS:
        klist = keywords.get(domain, [])
        overall[domain] = count_keywords(all_text, klist)

    print("Overall keyword hits across all QoL text:")
    for domain in DOMAINS:
        print(f"  {domain}: {overall[domain]}")
