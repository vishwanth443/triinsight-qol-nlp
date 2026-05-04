# app/bow_data.py

from pathlib import Path
import json
from sklearn.feature_extraction.text import CountVectorizer

DOMAINS = [
    "symptoms",
    "body_image",
    "mental_health",
    "interpersonal_relationships",
    "employment",
]


def load_patient(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_domain_texts(patient: dict) -> dict:
    q = patient["quality_of_life"]["free_text"]
    return {domain: q.get(domain, "") for domain in DOMAINS}


def load_texts(data_root: Path):
    texts = []
    ids = []

    real_dir = data_root / "real"
    for jf in sorted(real_dir.glob("*.json")):
        patient = load_patient(jf)
        q = patient["quality_of_life"]["free_text"]
        text = " ".join(q.get(d, "") for d in DOMAINS)
        texts.append(text)
        ids.append(patient.get("patient_id", jf.stem))

    return texts, ids


def build_patient_vectorizer(domain_texts: dict) -> CountVectorizer:
    corpus = [domain_texts[d] for d in DOMAINS]
    vectorizer = CountVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 1)
    )
    vectorizer.fit(corpus)
    return vectorizer


def vectorize_domain_text(text: str, vectorizer: CountVectorizer) -> dict:
    X = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    counts = X.toarray()[0]
    return {feature_names[i]: int(counts[i]) for i in range(len(feature_names))}


def compute_domain_bow_scores(json_path: Path):
    patient = load_patient(json_path)
    patient_id = patient.get("patient_id", json_path.stem)
    domain_texts = get_domain_texts(patient)

    vectorizer = build_patient_vectorizer(domain_texts)

    domain_scores = {}
    domain_vectors = {}

    for domain in DOMAINS:
        text = domain_texts[domain]
        vector_dict = vectorize_domain_text(text, vectorizer)

        bow_score = sum(vector_dict.values())

        domain_scores[domain] = bow_score
        domain_vectors[domain] = vector_dict

    return patient_id, domain_texts, domain_scores, domain_vectors

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        data_root = Path("data")
        texts, ids = load_texts(data_root)

        print("Patients:", ids)

        vectorizer = CountVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 1)
        )

        X = vectorizer.fit_transform(texts)
        vocab = vectorizer.get_feature_names_out()

        print("Vocabulary size:", len(vocab))
        print("Some example words:", vocab[:20])

    else:
        json_path = Path(sys.argv[1])
        patient_id, domain_texts, domain_scores, domain_vectors = compute_domain_bow_scores(json_path)

        print(f"\nPatient: {patient_id} ({json_path.name})\n")
        for domain in DOMAINS:
            print(f"[{domain}] bow_score={domain_scores[domain]}")
            print(f" text: {domain_texts[domain]}")
            print()