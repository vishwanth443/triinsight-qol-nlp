from pathlib import Path
import json
from sklearn.feature_extraction.text import CountVectorizer


MENTAL_HEALTH_SCALE = [
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


def load_patient(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------
# 1. Extractors for both formats
# -------------------------------
def extract_old_format_mental_health(patient: dict, fallback_id: str) -> tuple[str, str]:
    """
    Old structure: S001.json, p001.json
    {
        "patient_id": "...",
        "quality_of_life": {
            "free_text": {
                "mental_health": "..."
            }
        }
    }
    """
    patient_id = patient.get("patient_id", fallback_id)
    text = patient["quality_of_life"]["free_text"]["mental_health"]
    return patient_id, text


def extract_new_format_mental_health(
    dataset: list, patient_index: int, fallback_id: str
) -> tuple[str, str]:
    """
    New structure: realistic_synthetic_qol_patients_dataset_100_samples.json
    [
      {
        "Patient_ID": "...",
        "Narratives": {
            "MentalHealth_Affected_Elaborate": "... or 'N/A'",
            "MentalHealth_Coping_Strategies": "... or 'N/A'"
        }
      },
      ...
    ]
    """
    record = dataset[patient_index]
    patient_id = record.get("Patient_ID", fallback_id)

    narratives = record.get("Narratives", {})

    mh_aff = narratives.get("MentalHealth_Affected_Elaborate", "") or ""
    mh_coping = narratives.get("MentalHealth_Coping_Strategies", "") or ""

    # Clean up "N/A" and surrounding quotes
    def clean(s: str) -> str:
        s = s.strip()
        if s.upper() == "N/A":
            return ""
        # drop leading/trailing quotes if present
        if len(s) >= 2 and s[0] == s[-1] == '"':
            s = s[1:-1]
        return s

    mh_aff = clean(mh_aff)
    mh_coping = clean(mh_coping)

    text = " ".join(t for t in [mh_aff, mh_coping] if t)
    return patient_id, text


def extract_mental_health_text(json_path: Path, patient_index: int = 0) -> tuple[str, str]:
    """
    Auto-detect format:
    - If top-level is a dict with quality_of_life.free_text.mental_health -> old format
    - If top-level is a list with Patient_ID / Narratives.* -> new format
    """
    data = load_patient(json_path)

    # Old single-patient format
    if isinstance(data, dict) and "quality_of_life" in data:
        return extract_old_format_mental_health(data, json_path.stem)

    # New dataset format (list of records)
    if isinstance(data, list):
        return extract_new_format_mental_health(data, patient_index, json_path.stem)

    # Fallback: nothing usable
    return json_path.stem, ""


# -------------------------------
# 2. BOW + fuzzy logic (unchanged)
# -------------------------------
def compute_mental_health_bow_score(text: str) -> tuple[int, dict]:
    vectorizer = CountVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 1),
    )

    if not text.strip():
        return 0.0, {}

    X = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    counts = X.toarray()[0]

    bow_vector = {feature_names[i]: int(counts[i]) for i in range(len(feature_names))}
    total_tokens = float(sum(counts))

    # SCALE STEP (no logic change, just range normalisation)
    # Put k roughly into [0, 5] so that 0–2–4 region is meaningful.
    # For short QoL sentences: k ≈ 0–3
    # For long narratives: k ≈ 3–5
    k = total_tokens / 10.0

    return k, bow_vector
    
    
    bow_score = int(sum(counts))
    return bow_score, bow_vector


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
    else:
        return max(0.0, (4 - k) / 2.0)


def mu_high(k: float) -> float:
    if k <= 2:
        return 0.0
    elif 2 < k < 4:
        return (k - 2) / 2.0
    else:
        return 1.0


def severity_from_k(k: float) -> float:
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


def classify_mental_state(severity: float) -> str:
    if severity >= 0.93:
        return "Burnout"
    elif severity >= 0.86:
        return "Overwhelmed"
    elif severity >= 0.78:
        return "Distressed"
    elif severity >= 0.70:
        return "Struggling"
    elif severity >= 0.60:
        return "Stressed"
    elif severity >= 0.50:
        return "Low"
    elif severity >= 0.42:
        return "Tense"
    elif severity >= 0.34:
        return "Stable"
    elif severity >= 0.27:
        return "Balanced"
    elif severity >= 0.20:
        return "Calm"
    elif severity >= 0.14:
        return "Relaxed"
    elif severity >= 0.08:
        return "Positive"
    elif severity >= 0.03:
        return "Peaceful"
    else:
        return "Flourishing"


# -------------------------------
# 3. Main analysis API
# -------------------------------
def analyse_mental_health_only(json_path: Path, patient_index: int = 0) -> dict:
    patient_id, text = extract_mental_health_text(json_path, patient_index)
    bow_score, bow_vector = compute_mental_health_bow_score(text)

    low = mu_low(bow_score)
    med = mu_medium(bow_score)
    high = mu_high(bow_score)

    severity = severity_from_k(bow_score)
    flag = severity_to_flag(severity)
    mental_state = classify_mental_state(severity)

    return {
        "patient_id": patient_id,
        "text": text,
        "bow_score": bow_score,
        "bow_vector": bow_vector,
        "mu_low": round(low, 3),
        "mu_medium": round(med, 3),
        "mu_high": round(high, 3),
        "severity": round(severity, 3),
        "flag": flag,
        "mental_state": mental_state,
    }


def print_mental_health_result(result: dict):
    print(f"\nPatient: {result['patient_id']}")
    print("\n[Mental Health Only]")
    print(f"text: {result['text']}")
    print(f"bow_score: {result['bow_score']}")
    print(f"mu_low: {result['mu_low']}")
    print(f"mu_medium: {result['mu_medium']}")
    print(f"mu_high: {result['mu_high']}")
    print(f"severity: {result['severity']}")
    print(f"flag: {result['flag']}")
    print(f"mental_state: {result['mental_state']}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python -m app.mental_health_member_function data/real/S001.json")
        print("  python -m app.mental_health_member_function realistic_synthetic_qol_patients_dataset_100_samples.json 0")
        raise SystemExit(1)

    json_path = Path(sys.argv[1])

    # Optional patient index for the 100-sample dataset
    if len(sys.argv) >= 3:
        idx = int(sys.argv[2])
    else:
        idx = 0

    result = analyse_mental_health_only(json_path, idx)
    print_mental_health_result(result)