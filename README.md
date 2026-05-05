# Triinsight — NLP for QoL Patient’s Narrative Analysis

## Overview

Triinsight is a group project focused on **NLP for QoL Patient’s narrative analysis**. The project processes patient free-text responses and converts them into structured outputs that help assess the impact of abdominal wall hernia on quality of life across multiple domains using Bag of Words processing, fuzzy logic severity scoring, summary generation, and graph plotting for mental health analysis.[file:1][file:2][file:3][file:4]

The system works on patient narrative text stored in JSON format and analyses five Quality of Life domains: symptoms, body image, mental health, interpersonal relationships, and employment. These domains are explicitly defined in the project code and supporting documentation.[file:1][file:9]

## Project Aim

**Project Aim:** NLP for QoL Patient’s narrative analysis.

The purpose of the project is to analyse patient narratives and transform unstructured text into interpretable outputs such as severity values, domain-based concern levels, report text, and visual mental-health membership graphs. The project uses NLP-based text representation and fuzzy inference to make domain-level analysis easier to read and interpret.[file:1][file:2][file:3]

## Team

**Group Name:** Triinsight

### Team Members and Contributions

| Name | Contribution |
|---|---|
| Deepak Ravi | End-to-end pipeline integration, execution workflow, mental health analysis support, and local testing of patient-level runs. |
| Vishwanth Paka | Bag of Words text processing, JSON data handling, patient text preparation, and command-line execution support. |
| Panideep Kumar Reddy Kancham Reddy | Fuzzy logic modelling, severity and flag generation, summary report generation, and project documentation structure. |

## Core Working Modules

The current project contains the following main working modules.[file:1][file:2][file:3][file:4][file:5]

### `app/bow_data.py`

This module loads patient JSON files, reads the text from the five QoL domains, combines the text where needed, and applies `CountVectorizer` from scikit-learn to build a Bag of Words representation and vocabulary output.[file:1]

### `app/fuzzy_flags.py`

This module performs the fuzzy-logic-based domain analysis. It calculates low, medium, and high membership values from the domain evidence score, converts them into a severity score, and maps that score into a flag category.[file:2]

### `app/summary_report.py`

This module generates a narrative summary report from the analysed patient results. It builds domain-level summary text, overall assessment text, and recommendation text based on severity values.[file:3]

### `app/patient_report.py`

This is the main combined execution file for a patient-level run. It calls the fuzzy analysis module, prints detailed per-domain results, and then prints the narrative summary report.[file:4]

### `app/mental_health_member_function.py`

This module is used for focused mental-health-only analysis. It processes mental health text, computes a Bag of Words score, applies fuzzy severity logic, and outputs a mental health state. It is also the base module used for graph plotting support in the mental health graph files you created locally.[file:4]

## QoL Domains Used in the Project

The project analyses the following five domains.[file:1][file:9]

| Domain | Description |
|---|---|
| Symptoms | Physical pain, discomfort, movement restriction, and limitations in day-to-day activities.[file:9] |
| Body image | Self-consciousness, embarrassment, appearance-related concerns, and concealment behaviour.[file:9] |
| Mental health | Low mood, anxiety, emotional distress, coping difficulty, and psychological impact.[file:9] |
| Interpersonal relationships | Social withdrawal, family or partner effects, intimacy issues, and relationship strain.[file:9] |
| Employment | Work difficulty, role limitation, loss of ability to work, and financial impact.[file:9] |

## How the Project Works

### Step 1 — Input loading

The project loads patient JSON files from local storage. The text is read from the `quality_of_life.free_text` section, where each domain is stored separately.[file:1][file:2][file:4]

### Step 2 — Text processing

The project applies a Bag of Words approach using `CountVectorizer` from scikit-learn. This converts the patient narrative into token-based text features that can be analysed computationally.[file:1]

### Step 3 — Severity modelling

The project applies fuzzy membership functions (`mu_low`, `mu_medium`, `mu_high`) to transform the domain evidence score into a severity value. This severity is then mapped to a flag category such as blue, green, amber, red, or dark red.[file:2]

### Step 4 — Report generation

After severity is calculated for the patient domains, the project produces a readable patient summary report. This report explains the likely impact of the condition across the analysed domains and gives an overall assessment.[file:3][file:4]

### Step 5 — Graph plotting

The mental health part of the project can also be visualised through plotting scripts built on top of the mental health analysis module. These graphs are used to visualise the complete mental health membership functions and patient-specific mental health positioning on the membership graph.

## Architecture

The overall project architecture can be represented as follows based on the current code structure and execution flow.[file:1][file:2][file:3][file:4]

```text
                    +----------------------+
                    |   Patient JSON File  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |   Text Extraction    |
                    | quality_of_life text |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  Bag of Words Layer  |
                    |  CountVectorizer     |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
      +----------------------+     +----------------------+
      | Fuzzy Logic Analysis |     | Mental Health Module |
      | severity + flags     |     | focused MH analysis  |
      +----------+-----------+     +----------+-----------+
                 |                           |
                 v                           v
      +----------------------+     +----------------------+
      | Summary Report       |     | Plotting / Graphs    |
      | patient report text  |     | membership graphs    |
      +----------------------+     +----------------------+
```

## Project Structure

```text
awh-qol-nlp/
├── app/
│   ├── __init__.py
│   ├── bow_data.py
│   ├── fuzzy_flags.py
│   ├── fuzzy_plot.py
│   ├── mental_health_member_function.py
│   ├── patient_report.py
│   ├── plot_full_mental_health_membership.py
│   ├── plot_mental_health_function.py
│   └── summary_report.py
├── data/
│   ├── real/
│   |   ├── p001.json
│   |   ├── p002.json
│   |   └── ...
|   └── synthetic/
│       ├── S001.json
│       ├── S002.json
|       └── ...
└── qol_domains.md
```

The plotting files are included here because they are part of the working local version you have been building around the mental health analysis flow.

## Requirements

The verified dependency used directly in the uploaded code is:

- Python 3.9 or later is recommended.[file:5]
- `scikit-learn` for `CountVectorizer` and Bag of Words processing.[file:1]

For graph plotting in the local plotting files, install:

- `matplotlib`
- `numpy`

## Installation

### Clone the repository

```bash
git clone <your-repository-url>
cd awh-qol-nlp
```

### Create and activate a virtual environment

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

### Install dependencies

```bash
python -m pip install --upgrade pip
pip install scikit-learn numpy matplotlib
```

## How to Run

Run commands from the root project folder.

### Main patient run

```bash
python -m app.patient_report data/real/S001.json
```

This runs the full patient-level analysis and prints domain severities and the generated report text.[file:4]

### Run another patient file

```bash
python -m app.patient_report data/real/p001.json
```

### Run Bag of Words vocabulary analysis

```bash
python -m app.bow_data
```

This prints the patient IDs, vocabulary size, and sample words from the Bag of Words model.[file:1]

### Run fuzzy logic analysis only

```bash
python -m app.fuzzy_flags data/real/p001.json
```

This prints domain-level severity values, flag categories, and labels.[file:2]

### Run summary report only

```bash
python -m app.summary_report data/real/p001.json
```

This prints the narrative summary report only.[file:3]

### Run mental-health-only analysis

```bash
python -m app.mental_health_member_function data/real/S001.json
```

### Run full mental health membership graph

```bash
python -m app.plot_full_mental_health_membership
```

This displays the complete mental health membership function graph.

### Run patient-specific mental health graph

```bash
python -m app.plot_mental_health_function data/real/S001.json
```

This displays the patient position on the mental health membership graph.

## Expected Input Format

The expected patient JSON structure for the main patient-level modules is:

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
    }
  }
}
```

This structure matches how the uploaded modules load and analyse patient narratives.[file:1][file:2][file:4]

## Output Produced

The project can produce the following outputs depending on which module is run:

- Bag of Words vocabulary output.[file:1]
- Domain-level severity values.[file:2]
- Fuzzy flag categories.[file:2]
- Mental health state output from the mental health module.
- Narrative patient summary report text.[file:3][file:4]
- Full membership graphs and patient-level mental health plots through the plotting modules.

## End-to-End Flow

A typical project run follows this order:

1. Load patient JSON input.[file:1][file:4]
2. Extract domain-specific free text.[file:1][file:2]
3. Convert text into Bag of Words representation.[file:1]
4. Apply fuzzy membership functions for severity scoring.[file:2]
5. Generate flags and domain-level interpretation.[file:2]
6. Build the final textual patient report.[file:3][file:4]
7. Optionally visualise mental health membership functions through graph plotting.

## Notes

- Run every command from the project root directory for module imports and relative paths to work correctly.[file:4][file:3][file:2]
- The `app` folder should contain `__init__.py` if you are using `python -m app...` commands.[file:4]
- The plotting scripts depend on the mental health analysis module and should be kept inside the `app` package.

## Summary

Triinsight’s project provides a structured NLP pipeline for analysing QoL patient narratives using Bag of Words processing, fuzzy severity modelling, report generation, and mental health graph plotting. The system is organised around five QoL domains and is designed to turn patient narrative text into clear analytical and visual outputs that can support interpretation of quality-of-life impact.[file:1][file:2][file:3][file:4][file:9]
