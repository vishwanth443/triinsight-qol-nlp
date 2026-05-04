from pathlib import Path
import json
from collections import Counter

from app.bow_data import load_patient, DOMAINS


def load_keywords(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def count_keywords(text: str, keywords: list[str]) -> int:
    text_l = text.lower()
    count = 0
    for kw in keywords:
        if kw in text_l:
            count += 1
    return count


def keyword_count_to_flag_and_label(k: int) -> tuple[str, int]:
    """
    Manual 'decision tree' for a domain:

    k >= 3  -> red,   label 1 (domain clearly affected)
    k == 1-2 -> amber, label 1 (some concern)
    k == 0  -> green, label 0 (not clearly affected)
    """
    if k >= 3:
        return "red", 1
    elif k >= 1:
        return "amber", 1
    else:
        return "green", 0


def analyse_patient_manual(json_path: Path, keywords_path: Path):
    patient = load_patient(json_path)
    patient_id = patient.get("patient_id", json_path.stem)
    q = patient["quality_of_life"]["free_text"]

    keywords = load_keywords(keywords_path)

    results = {}
    for domain in DOMAINS:
        text = q[domain]
        kw_list = keywords.get(domain, [])
        hits = count_keywords(text, kw_list)
        flag, label = keyword_count_to_flag_and_label(hits)
        results[domain] = {
            "keyword_hits": hits,
            "flag": flag,
            "label": label,
            "text": text
        }

    return patient_id, results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m app.manual_tree data/real/p001.json")
        raise SystemExit(1)

    json_path = Path(sys.argv[1])
    keywords_path = Path("config/keywords.json")

    pid, results = analyse_patient_manual(json_path, keywords_path)

    print(f"\nPatient: {pid} ({json_path.name})\n")
    for domain, info in results.items():
        print(
            f"[{domain}] flag={info['flag']}  "
            f"label={info['label']}  "
            f"keyword_hits={info['keyword_hits']}"
        )
        print(f"  text: {info['text']}\n")
