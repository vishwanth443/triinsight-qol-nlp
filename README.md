# Triinsight — NLP for QoL Patient’s Narrative Analysis

## Overview

This project focuses on **Natural Language Processing (NLP) for Quality of Life (QoL) patient narrative analysis**. It processes patient free-text responses and analyses how abdominal wall hernia affects different areas of daily life using a Bag of Words approach, keyword matching, and fuzzy logic-based severity scoring.[1][2][3][4]

The system is designed to examine patient narratives across five Quality of Life domains: symptoms, body image, mental health, interpersonal relationships, and employment. Each domain is analysed separately so the output can show domain-level impact, severity, and flag status.[1][5][4]

## Project Aim

**Project Aim:** NLP for QoL Patient’s narrative analysis.

The goal of the project is to convert unstructured patient narrative text into structured indicators that help identify how strongly different QoL domains are affected. The project uses text processing to detect domain-relevant expressions, then applies fuzzy logic to transform keyword evidence into severity levels and clinical-style flags.[2][3][5][4]

## Team

**Group Name:** Triinsight

### Team Members and Contributions

| Name | Contribution |
|---|---|
| Deepak Ravi | NLP pipeline integration, patient-level execution flow, command-line run structure, and coordination of end-to-end local testing. |
| Vishwanth Paka | Bag of Words processing, keyword-based domain counting, JSON input handling, and domain text preparation. |
| Panideep Kumar Reddy Kancham Reddy | Fuzzy logic severity mapping, flag generation, reporting logic, and summary report generation. |

## What the Project Does

The project reads patient JSON files containing QoL free-text responses. It extracts narrative text for the five predefined domains and processes them through a structured analysis pipeline.[1][3][4]

The current workflow supports:

- Loading patient JSON files from local storage.[1][3]
- Extracting QoL free-text content from domain-specific fields.[1][2][3]
- Building a Bag of Words representation of text using `CountVectorizer` from scikit-learn.[1]
- Counting domain-specific keywords using a configurable keyword dictionary stored in `config/keywords.json`.[2][6][5]
- Applying fuzzy membership functions to convert keyword hits into severity scores and colour-style flags.[2]
- Producing a patient-level summary report that describes impact across symptoms, body image, mental health, relationships, and employment.[7][3]

## QoL Domains Analysed

The analysis is organised around five QoL domains defined in the project files.[1][4]

| Domain | Purpose |
|---|---|
| Symptoms | Measures physical effects such as pain, restricted movement, discomfort, and daily activity limitation.[5][4] |
| Body image | Captures self-consciousness, embarrassment, shame, concealment, and appearance-related concerns.[5][4] |
| Mental health | Captures low mood, anxiety, distress, coping difficulty, and emotionally negative reactions.[5][4] |
| Interpersonal relationships | Captures social withdrawal, family and partner impact, awkwardness, intimacy issues, and relationship strain.[5][4] |
| Employment | Captures work limitations, role changes, financial pressure, income issues, and reduced ability to work.[5][4] |

## How the System Works

### 1. Input structure

The project expects patient data in JSON format. The main analysis files read patient narratives from the `quality_of_life.free_text` section, where each QoL domain is stored as a separate text field.[1][2][3]

The expected domain keys are:

- `symptoms` [1]
- `body_image` [1]
- `mental_health` [1]
- `interpersonal_relationships` [1]
- `employment` [1]

### 2. Bag of Words processing

The project uses `CountVectorizer` from scikit-learn to transform patient text into tokenised vocabulary features. This forms the NLP foundation for domain-level text processing and vocabulary inspection.[1]

### 3. Keyword-based domain evidence

A configurable keyword list is stored in `config/keywords.json`, with separate keywords for each QoL domain. The keyword counting step checks whether domain-relevant expressions appear in the patient’s narrative text and computes keyword hit counts for each domain.[6][5]

### 4. Fuzzy logic severity scoring

The project applies fuzzy membership functions to keyword hit counts. Three membership levels are used — low, medium, and high — and these are combined through a weighted severity function to generate a severity score between 0 and 1.[2]

The severity score is then mapped to a flag category:

- `blue` for very low concern.[2]
- `green` for low concern.[2]
- `amber` for medium concern.[2]
- `red` for high concern.[2]
- `dark_red` for very high concern.[2]

### 5. Report generation

After domain-level analysis is complete, the project can generate a narrative summary report. The report combines severity values across domains and produces an overall assessment plus a follow-up recommendation statement.[7][3]

## Project Structure

```text
awh-qol-nlp/
├── app/
│   ├── __init__.py
│   ├── bow_data.py
│   ├── keyword_counts.py
│   ├── fuzzy_flags.py
│   ├── summary_report.py
│   ├── plot_full_mental_health_membership.py
│   ├── plot_mental_health_function.py
│   ├── patient_report.py
│   └── mental_health_member_function.py
├── config/
│   └── keywords.json
├── data/
│   └── real/
│       ├── S001.json
│       ├── p001.json
│       └── ...
└── qol_domains.md
```

This structure matches the project code layout, where Python modules are imported through the `app` package and keyword configuration is read from `config/keywords.json`.[3][2][7][6]

## Main Python Files

### `app/bow_data.py`

This file defines the five core QoL domains, loads patient JSON files, combines domain text, and builds a Bag of Words vocabulary using `CountVectorizer`.[1]

### `app/keyword_counts.py`

This file loads the keyword dictionary and counts keyword hits within each domain. It is useful for checking how much domain-specific evidence exists in a patient narrative.[6][5]

### `app/fuzzy_flags.py`

This file applies fuzzy membership functions to keyword hit counts and generates per-domain severity values, flags, and binary labels.[2]

### `app/summary_report.py`

This file produces a human-readable textual report based on the domain-level results. It includes domain summaries, an overall assessment, and a referral-style recommendation.[7]

### `app/patient_report.py`

This file is the main patient-level demo runner. It combines fuzzy domain analysis with summary report generation and prints detailed results plus the final narrative report.[3]

### `app/mental_health_member_function.py`

This file is used for focused mental-health-only analysis and can be extended with plotting scripts for visualising the mental health membership function and related outputs. [3]

## Requirements

The uploaded code directly requires the following verified dependency:

- Python 3.9 or later is recommended because the project uses modern Python syntax such as `list[str]` type annotations.[6]
- `scikit-learn` is required for the Bag of Words implementation using `CountVectorizer`.[1]

Standard library modules used in the project include:

- `json` [1][2][6]
- `pathlib` [1][2][7][3][6]
- `collections` [6]

If plotting files are included locally, `matplotlib` and `numpy` may also be required for graph generation. This depends on whether those plotting scripts are part of the local project version.

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd awh-qol-nlp
```

### 2. Create a virtual environment

**Windows Command Prompt**

```bat
py -3 -m venv .venv
.venv\Scripts\activate
```

**PowerShell**

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install required packages

```bash
python -m pip install --upgrade pip
pip install scikit-learn
```

If graph plotting files are present in the local project version, install:

```bash
pip install matplotlib numpy
```

## How to Run the Project

Run all commands from the project root directory so that relative paths such as `config/keywords.json` work correctly.[2][7][3][6]

### Main demo run

The main end-to-end demo run is:

```bash
python -m app.patient_report data/real/S001.json
```

This runs the full domain analysis, prints domain results, and generates the narrative patient summary report.[3]

### Run with another patient JSON file

```bash
python -m app.patient_report data/real/p001.json
```

### Run Bag of Words vocabulary inspection

```bash
python -m app.bow_data
```

This loads available patient files from `data/real/`, builds the text corpus, and prints vocabulary information.[1]

### Run keyword counting only

```bash
python -m app.keyword_counts data/real/p001.json
```

This prints per-domain keyword hit counts and overall keyword coverage across the patient text.[6]

### Run fuzzy severity and flags only

```bash
python -m app.fuzzy_flags data/real/p001.json
```

This prints domain-level fuzzy severity values, flags, keyword hits, and labels.[2]

### Run summary report only

```bash
python -m app.summary_report data/real/p001.json
```

This generates the narrative summary report without the full detailed patient-report wrapper.[7]

### Run mental-health-only module

```bash
python -m app.mental_health_member_function data/real/S001.json
```

If the local mental health file supports indexed dataset input, it can also be run with a second numeric argument for patient selection in list-based JSON files.

## Expected Input Format

The patient JSON format should include:

```json
{
  "patient_id": "P001",
  "quality_of_life": {
    "free_text": {
      "symptoms": "...",
      "body_image": "...",
      "mental_health": "...",
      "interpersonal_relationships": "...",
      "employment": "..."
    },
    "labels": {
      "symptoms": 0,
      "body_image": 0,
      "mental_health": 0,
      "interpersonal_relationships": 0,
      "employment": 0
    }
  }
}
```

The analysis modules primarily depend on `patient_id` and `quality_of_life.free_text`. Label fields may exist for reference, but the fuzzy scoring modules derive their own outputs from text and keyword evidence.[2][3][8][9]

## Output Produced

Depending on the file being run, the project can produce:

- Domain-level keyword hit counts.[6]
- Fuzzy severity values for each domain.[2]
- Flag categories such as blue, green, amber, red, and dark red.[2]
- Binary labels derived from severity thresholds.[2]
- Human-readable summary report text.[7][3]
- Vocabulary inspection from Bag of Words processing.[1]

## Example Analysis Flow

A typical project run follows this sequence:

1. Load patient JSON data.[1][3]
2. Read free-text narratives for the five QoL domains.[1][2]
3. Count domain-related keywords using the configured dictionary.[6][5]
4. Convert keyword hit counts into fuzzy severity scores.[2]
5. Map severity scores into coloured flags.[2]
6. Generate a domain summary and an overall textual report.[7][3]

## Notes for Local Execution

- Run commands from the root folder of the project so relative file paths resolve correctly.[3][2][7][6]
- Ensure `keywords.json` is placed inside the `config/` directory.[2][6][5]
- Ensure patient JSON files are stored in the correct data directory before execution.[1][3]
- If using package-style commands such as `python -m app.patient_report`, the `app/` folder should include `__init__.py`.[3]

## Summary

Triinsight’s **NLP for QoL Patient’s narrative analysis** project provides a structured pipeline for analysing patient free-text narratives across clinically meaningful QoL domains. It combines Bag of Words text processing, domain keyword evidence, fuzzy severity scoring, and narrative report generation to transform unstructured patient text into interpretable analytical outputs.[1][2][7][3][4]
