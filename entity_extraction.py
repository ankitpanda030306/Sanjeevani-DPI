"""
Stage 1: Clinical Entity Isolation.

Rule-based extractor that:
  1. Splits raw clinical narrative into clauses.
  2. Detects negation cues (e.g. "no", "denies", "without", "ruled out")
     and marks any symptom phrase inside a negated clause as inactive,
     so it is never passed downstream as an active complaint.
  3. Returns cleaned candidate symptom phrases for semantic retrieval.

This module is intentionally dependency-free (no LLM call) so the pipeline
is fully deterministic and reproducible for the benchmark. Swap in an LLM
few-shot extractor here if you want richer phrase segmentation - as long
as it still runs negated spans through `is_negated()` before they reach
the retrieval stage.
"""

import re
from dataclasses import dataclass, field
from typing import List

NEGATION_CUES = [
    "no ", "not ", "denies", "denied", "without", "ruled out", "rule out",
    "negative for", "absence of", "free of", "no evidence of",
]

# Split narrative into clauses on common conjunctions / punctuation.
CLAUSE_SPLIT_RE = re.compile(r"[.;]|(?:\bbut\b)|(?:\band\b)|,")

# A small controlled symptom vocabulary used to pull candidate phrases out
# of free text. This is deliberately simple/regex-based; a production
# system would use a clinical NER model (e.g. scispaCy) here instead.
SYMPTOM_VOCAB = [
    "fever", "high fever", "cough", "chronic cough", "chest pain",
    "breathlessness", "wheezing", "diarrhea", "loose motions",
    "loose motion", "watery stools", "vomiting", "stomach cramps",
    "blood in stool", "joint pain", "rash", "chills", "sweating",
    "night sweats", "weight loss", "frequent urination", "headache",
    "high blood pressure", "bp high", "yellow skin", "yellow eyes",
    "yellowish discoloration", "pallor", "weakness", "fatigue",
]

# Common typo / shorthand normalisation seen in rural clinical notes.
NORMALISATION_MAP = {
    "sugar problm": "high blood sugar",
    "freqent urination": "frequent urination",
    "wt loss": "weight loss",
    "n wt": "and weight",
}


@dataclass
class ExtractedEntity:
    phrase: str
    negated: bool = False


@dataclass
class ExtractionResult:
    active_complaints: List[str] = field(default_factory=list)
    negated_mentions: List[str] = field(default_factory=list)
    raw_clauses: List[str] = field(default_factory=list)


def _normalise(text: str) -> str:
    text = text.lower()
    for typo, fix in NORMALISATION_MAP.items():
        text = text.replace(typo, fix)
    return text


def _clause_is_negated(clause: str) -> bool:
    return any(cue in clause for cue in NEGATION_CUES)


def extract_entities(narrative: str) -> ExtractionResult:
    """
    Parse a raw clinical narrative into active vs. negated symptom mentions.
    """
    text = _normalise(narrative)
    clauses = [c.strip() for c in CLAUSE_SPLIT_RE.split(text) if c.strip()]

    result = ExtractionResult(raw_clauses=clauses)
    seen_active, seen_negated = set(), set()

    for clause in clauses:
        negated = _clause_is_negated(clause)
        for symptom in SYMPTOM_VOCAB:
            if symptom in clause:
                if negated:
                    if symptom not in seen_negated:
                        seen_negated.add(symptom)
                        result.negated_mentions.append(symptom)
                else:
                    if symptom not in seen_active:
                        seen_active.add(symptom)
                        result.active_complaints.append(symptom)

    return result


if __name__ == "__main__":
    sample = "Patient has fever, but no diarrhea or vomiting."
    res = extract_entities(sample)
    print("Active:", res.active_complaints)
    print("Negated:", res.negated_mentions)
