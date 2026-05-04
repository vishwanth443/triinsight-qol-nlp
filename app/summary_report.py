# app/summary_report.py

from pathlib import Path
from app.fuzzy_flags import analyse_patient_fuzzy


def overall_assessment(results: dict) -> str:
    severities = [info["severity"] for info in results.values()]
    max_sev = max(severities) if severities else 0.0
    avg_sev = sum(severities) / len(severities) if severities else 0.0

    if max_sev >= 0.8 or avg_sev >= 0.7:
        return "High level of concern across multiple domains."
    elif max_sev >= 0.6 or avg_sev >= 0.5:
        return "Moderate level of concern with some domains significantly affected."
    elif max_sev >= 0.4 or avg_sev >= 0.3:
        return "Mild to moderate concerns in specific domains."
    else:
        return "Low overall level of concern."


def referral_recommendation(results: dict) -> str:
    flags = [info["flag"] for info in results.values()]
    severities = [info["severity"] for info in results.values()]
    max_sev = max(severities) if severities else 0.0

    if "dark_red" in flags or max_sev >= 0.85:
        return (
            "RED FLAG – Immediate medical follow-up is recommended, including "
            "evaluation by a surgical specialist and mental health support."
        )

    if "red" in flags or max_sev >= 0.7:
        return (
            "AMBER/RED FLAG – Prompt medical review is recommended to monitor "
            "symptoms and consider referral for psychological support."
        )

    if "amber" in flags or max_sev >= 0.5:
        return (
            "AMBER FLAG – Medical review is advisable to monitor impact and "
            "adjust management if needed."
        )

    return (
        "GREEN/BLUE FLAG – Routine follow-up is appropriate unless new or "
        "worsening symptoms arise."
    )


def build_summary_text(pid: str, results: dict) -> str:
    lines = []
    lines.append("Patient Summary Report\n")

    symp = results.get("symptoms", {})
    if symp.get("severity", 0) > 0.7:
        lines.append(
            "The patient reports significant limitations in daily activities "
            "due to persistent pain and reduced mobility."
        )
    elif symp.get("severity", 0) > 0.4:
        lines.append(
            "The patient reports some impact on daily activities related to "
            "pain and physical symptoms."
        )
    else:
        lines.append(
            "Physical symptoms currently have limited impact on daily activities."
        )
    lines.append("")

    body = results.get("body_image", {})
    if body.get("severity", 0) > 0.7:
        lines.append(
            "There are strong concerns related to body image, with the "
            "patient expressing discomfort and self-consciousness about "
            "appearance."
        )
    elif body.get("severity", 0) > 0.4:
        lines.append(
            "The patient expresses some concerns about body image and "
            "appearance."
        )
    else:
        lines.append(
            "Body image does not appear to be a major concern at present."
        )
    lines.append("")

    mh = results.get("mental_health", {})
    if mh.get("severity", 0) > 0.7:
        lines.append(
            "The patient shows significant mental health distress, including "
            "low mood and difficulty coping."
        )
    elif mh.get("severity", 0) > 0.4:
        lines.append(
            "Mental health indicators suggest mild to moderate distress, with "
            "some difficulties in coping."
        )
    else:
        lines.append(
            "Mental health symptoms are currently mild with no major distress reported."
        )
    lines.append("")

    rel = results.get("interpersonal_relationships", {})
    if rel.get("severity", 0) > 0.7:
        lines.append(
            "Social and interpersonal relationships are negatively affected, "
            "with reduced interaction and strain in personal relationships."
        )
    elif rel.get("severity", 0) > 0.4:
        lines.append(
            "The patient reports some strain in social and interpersonal "
            "relationships."
        )
    else:
        lines.append("Interpersonal relationships remain largely stable.")
    lines.append("")

    emp = results.get("employment", {})
    if emp.get("severity", 0) > 0.7:
        lines.append(
            "The patient has experienced major employment impact, including "
            "stopping work and financial difficulties."
        )
    elif emp.get("severity", 0) > 0.4:
        lines.append(
            "The condition has led to some work or financial impact, such as "
            "reduced hours or role changes."
        )
    else:
        lines.append("Employment and finances are currently largely maintained.")
    lines.append("")

    lines.append("Overall Assessment:")
    lines.append(overall_assessment(results))
    lines.append("")
    lines.append("Referral Recommendation:")
    lines.append(referral_recommendation(results))

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m app.summary_report data/real/p002.json")
        raise SystemExit(1)

    json_path = Path(sys.argv[1])
    pid, results = analyse_patient_fuzzy(json_path)
    report = build_summary_text(pid, results)
    print(report)