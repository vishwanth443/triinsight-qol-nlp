# app/patient_report.py

from pathlib import Path
from app.fuzzy_flags import analyse_patient_fuzzy
from app.summary_report import build_summary_text


def print_domain_results(pid: str, results: dict):
    print(f"\nPatient: {pid}\n")

    for domain, info in results.items():
        print(
            f"[{domain}] flag={info['flag']} "
            f"severity={info['severity']:.3f} "
            f"bow_score={info['bow_score']}"
        )

        text = info["text"]
        excerpt = text[:140].strip()
        if len(text) > 140:
            excerpt += "..."

        print(f" example: \"{excerpt}\"\n")


def main(json_path: Path):
    pid, results = analyse_patient_fuzzy(json_path)

    print_domain_results(pid, results)

    print("\n" + "=" * 70 + "\n")
    report_text = build_summary_text(pid, results)
    print(report_text)
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m app.patient_report data/real/S001.json")
        raise SystemExit(1)

    json_path = Path(sys.argv[1])
    main(json_path)