# Candidate Transformer

A configurable **ETL (Extract → Transform → Load)** pipeline that converts candidate information from multiple sources into a unified canonical profile.

The project combines:

- **Structured Data:** Recruiter CSV
- **Unstructured Data:** Resume PDF

The extracted information is normalized, merged, validated, and projected into different output schemas using a runtime configuration file **without modifying the application code**.

---

## Features

- Extract candidate data from CSV
- Extract information from Resume PDF
- Normalize candidate information
- Merge structured and unstructured data
- Conflict resolution with confidence scoring
- Provenance tracking
- Runtime configurable output schema
- Dynamic JSON Schema validation
- Generate multiple output formats using different configuration files

---

## Project Structure

```text
candidate-transformer/
│
├── input/
│   ├── recruiter.csv
│   ├── resume.pdf
│   ├── default_config.json
│   └── custom_config.json
│
├── output/
│   ├── canonical_output.json
│   └── custom_output.json
│
├── src/
│   ├── csv_extractor.py
│   ├── resume_extractor.py
│   ├── normalizer.py
│   ├── merger.py
│   ├── projector.py
│   ├── validator.py
│   └── main.py
│
├── tests/
│   └── test_merger.py
│
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10 or later

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Elavarasan2023IT014/Candidate-Transformer.git
```

### Navigate to the Project Directory

```bash
cd candidate-transformer
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Project

From the project root directory, execute:

```bash
python src/main.py
```

---

## Running Unit Tests

Install **pytest** (if not already installed):

```bash
pip install pytest
```

Run all tests:

```bash
pytest
```

Expected output:

```text
============================= test session starts =============================

tests/test_merger.py ....

============================== 4 passed ==============================
```

---

## Author

**Elavarasan R**