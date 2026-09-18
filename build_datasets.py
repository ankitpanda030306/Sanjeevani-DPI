"""
Builds the three deliverable datasets described in the spec:
  - master_icd10_registry.json
  - master_pmjay_tariffs.json
  - benchmark_ground_truth.json

This is a curated STARTER set (not the full 100-200 / 30-50 / 30-50 scope
required for the hackathon submission) covering every category called out
in the spec (infectious, respiratory, chronic, maternal/pediatric) plus
edge cases (negation, ambiguous multi-symptom, vernacular/slang, typos).
Extend each list below to hit the full target counts.
"""

import json
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# ---------------------------------------------------------------------------
# Dataset A: Clinical Diagnostic Ontology Master (ICD-10-CM & SNOMED-CT)
# ---------------------------------------------------------------------------
ICD10_REGISTRY = [
    {
        "concept_name": "Acute gastroenteritis",
        "icd10_code": "A09",
        "snomed_id": "25374005",
        "description": "Acute inflammation of the stomach and intestines causing diarrhea and vomiting.",
        "synonyms": ["watery diarrhea", "loose motions", "stomach infection",
                     "food poisoning", "loose motion", "watery stools"],
        "category": "Infectious disease",
    },
    {
        "concept_name": "Dengue fever",
        "icd10_code": "A90",
        "snomed_id": "38362002",
        "description": "Mosquito-borne viral infection causing high fever, rash, and severe joint/muscle pain.",
        "synonyms": ["breakbone fever", "high fever with body ache", "dengue",
                     "platelet drop fever"],
        "category": "Infectious disease",
    },
    {
        "concept_name": "Malaria",
        "icd10_code": "B54",
        "snomed_id": "61462000",
        "description": "Mosquito-borne parasitic disease causing cyclical fever, chills, and sweating.",
        "synonyms": ["malaria fever", "chills and fever", "cyclical fever"],
        "category": "Infectious disease",
    },
    {
        "concept_name": "Typhoid fever",
        "icd10_code": "A01.0",
        "snomed_id": "4834000",
        "description": "Bacterial infection (Salmonella typhi) causing prolonged fever and abdominal pain.",
        "synonyms": ["typhoid", "prolonged fever with abdominal pain", "enteric fever"],
        "category": "Infectious disease",
    },
    {
        "concept_name": "Cholera",
        "icd10_code": "A00",
        "snomed_id": "63650001",
        "description": "Acute bacterial intestinal infection causing severe watery diarrhea and dehydration.",
        "synonyms": ["rice-water stools", "severe watery diarrhea with dehydration"],
        "category": "Infectious disease",
    },
    {
        "concept_name": "Tuberculosis, pulmonary",
        "icd10_code": "A15.0",
        "snomed_id": "154283005",
        "description": "Chronic bacterial infection of the lungs causing persistent cough, weight loss, and night sweats.",
        "synonyms": ["TB", "chronic cough with weight loss", "night sweats and cough"],
        "category": "Infectious disease",
    },
    {
        "concept_name": "Bacterial pneumonia",
        "icd10_code": "J15.9",
        "snomed_id": "53084003",
        "description": "Bacterial infection of the lung causing fever, cough, and difficulty breathing.",
        "synonyms": ["chest infection", "pneumonia", "lung infection with fever"],
        "category": "Respiratory illness",
    },
    {
        "concept_name": "Acute bronchitis",
        "icd10_code": "J20.9",
        "snomed_id": "10509002",
        "description": "Inflammation of the bronchial tubes causing cough and mucus production.",
        "synonyms": ["chest cold", "bronchitis", "cough with phlegm"],
        "category": "Respiratory illness",
    },
    {
        "concept_name": "Asthma, unspecified",
        "icd10_code": "J45.909",
        "snomed_id": "195967001",
        "description": "Chronic airway inflammation causing wheezing, breathlessness, and chest tightness.",
        "synonyms": ["wheezing", "breathlessness with wheeze", "asthma attack"],
        "category": "Respiratory illness",
    },
    {
        "concept_name": "COPD",
        "icd10_code": "J44.9",
        "snomed_id": "13645005",
        "description": "Chronic obstructive pulmonary disease causing long-term breathing difficulty.",
        "synonyms": ["chronic breathlessness", "COPD", "smoker's lung"],
        "category": "Respiratory illness",
    },
    {
        "concept_name": "Type 2 diabetes mellitus",
        "icd10_code": "E11.9",
        "snomed_id": "44054006",
        "description": "Chronic metabolic disorder causing high blood sugar.",
        "synonyms": ["diabetes", "sugar", "high blood sugar", "polyuria", "diabetic checkup", "t2dm", "hyperglycemia"],
        "category": "Chronic condition",
    },
    {
        "concept_name": "Essential hypertension",
        "icd10_code": "I10",
        "snomed_id": "38341003",
        "description": "Chronic elevation of blood pressure.",
        "synonyms": ["high blood pressure", "BP high", "hypertension"],
        "category": "Chronic condition",
    },
    {
        "concept_name": "Ischemic heart disease",
        "icd10_code": "I25.9",
        "snomed_id": "414545008",
        "description": "Reduced blood supply to the heart muscle, often causing chest pain.",
        "synonyms": ["heart blockage", "chest pain on exertion", "IHD"],
        "category": "Chronic condition",
    },
    {
        "concept_name": "Normal delivery",
        "icd10_code": "O80",
        "snomed_id": "289096004",
        "description": "Uncomplicated vaginal delivery of a single healthy infant.",
        "synonyms": ["normal delivery", "vaginal delivery", "uncomplicated childbirth"],
        "category": "Maternal and pediatric",
    },
    {
        "concept_name": "Neonatal jaundice",
        "icd10_code": "P59.9",
        "snomed_id": "13835006",
        "description": "Yellowing of a newborn's skin and eyes due to elevated bilirubin.",
        "synonyms": ["baby jaundice", "yellow skin newborn", "neonatal jaundice"],
        "category": "Maternal and pediatric",
    },
    {
        "concept_name": "Iron-deficiency anemia",
        "icd10_code": "D50.9",
        "snomed_id": "87522002",
        "description": "Anemia caused by insufficient iron, causing fatigue and pallor.",
        "synonyms": ["low hemoglobin", "anemia", "weakness and pale skin"],
        "category": "Maternal and pediatric",
    },
]

# ---------------------------------------------------------------------------
# Dataset B: Ayushman Bharat Health Benefit Packages (AB-PMJAY Tariff Master)
# ---------------------------------------------------------------------------
PMJAY_TARIFFS = [
    {"package_code": "MED_INF_A09", "package_name": "Acute Gastroenteritis Management",
     "linked_icd10": "A09", "speciality": "General Medicine",
     "ceiling_inr": 4500, "pre_auth_required": False,
     "mandatory_investigations": ["Stool routine", "Serum electrolytes"]},
    {"package_code": "MED_INF_A90", "package_name": "Dengue Fever Management",
     "linked_icd10": "A90", "speciality": "General Medicine",
     "ceiling_inr": 8500, "pre_auth_required": False,
     "mandatory_investigations": ["CBC with platelet count", "NS1/IgM Dengue"]},
    {"package_code": "MED_INF_B54", "package_name": "Malaria Treatment",
     "linked_icd10": "B54", "speciality": "General Medicine",
     "ceiling_inr": 6000, "pre_auth_required": False,
     "mandatory_investigations": ["Peripheral smear", "Rapid malaria antigen test"]},
    {"package_code": "MED_INF_A010", "package_name": "Typhoid Fever Management",
     "linked_icd10": "A01.0", "speciality": "General Medicine",
     "ceiling_inr": 7000, "pre_auth_required": False,
     "mandatory_investigations": ["Widal test/blood culture"]},
    {"package_code": "MED_INF_A00", "package_name": "Cholera Management",
     "linked_icd10": "A00", "speciality": "General Medicine",
     "ceiling_inr": 9500, "pre_auth_required": True,
     "mandatory_investigations": ["Stool culture", "Serum electrolytes"]},
    {"package_code": "MED_INF_A150", "package_name": "Pulmonary Tuberculosis Treatment (DOTS)",
     "linked_icd10": "A15.0", "speciality": "Pulmonology",
     "ceiling_inr": 12000, "pre_auth_required": True,
     "mandatory_investigations": ["Sputum AFB / CBNAAT", "Chest X-ray"]},
    {"package_code": "MED_PNEUMONIA_J15", "package_name": "Bacterial Pneumonia Management",
     "linked_icd10": "J15.9", "speciality": "Pulmonology",
     "ceiling_inr": 15000, "pre_auth_required": True,
     "mandatory_investigations": ["Chest X-ray", "CBC"]},
    {"package_code": "MED_RESP_J209", "package_name": "Acute Bronchitis Management",
     "linked_icd10": "J20.9", "speciality": "Pulmonology",
     "ceiling_inr": 3500, "pre_auth_required": False,
     "mandatory_investigations": ["Chest X-ray (if indicated)"]},
    {"package_code": "MED_RESP_J45909", "package_name": "Acute Asthma Exacerbation Management",
     "linked_icd10": "J45.909", "speciality": "Pulmonology",
     "ceiling_inr": 5500, "pre_auth_required": False,
     "mandatory_investigations": ["Peak expiratory flow rate", "SpO2"]},
    {"package_code": "MED_RESP_J449", "package_name": "COPD Exacerbation Management",
     "linked_icd10": "J44.9", "speciality": "Pulmonology",
     "ceiling_inr": 18000, "pre_auth_required": True,
     "mandatory_investigations": ["Chest X-ray", "SpO2", "ABG (if severe)"]},
    {"package_code": "MED_CHR_E119", "package_name": "Type 2 Diabetes Mellitus Management",
     "linked_icd10": "E11.9", "speciality": "General Medicine",
     "ceiling_inr": 6000, "pre_auth_required": False,
     "mandatory_investigations": ["Fasting/PP blood glucose", "HbA1c"]},
    {"package_code": "MED_CHR_I10", "package_name": "Hypertension Management",
     "linked_icd10": "I10", "speciality": "General Medicine",
     "ceiling_inr": 4000, "pre_auth_required": False,
     "mandatory_investigations": ["Blood pressure monitoring", "ECG"]},
    {"package_code": "CARD_IHD_I259", "package_name": "Ischemic Heart Disease Management",
     "linked_icd10": "I25.9", "speciality": "Cardiology",
     "ceiling_inr": 25000, "pre_auth_required": True,
     "mandatory_investigations": ["ECG", "Troponin", "Echocardiogram"]},
    {"package_code": "OBS_NORMAL_O80", "package_name": "Normal Delivery Package",
     "linked_icd10": "O80", "speciality": "Obstetrics",
     "ceiling_inr": 9000, "pre_auth_required": False,
     "mandatory_investigations": ["Antenatal records", "Partograph"]},
    {"package_code": "PED_JAUNDICE_P599", "package_name": "Neonatal Jaundice Management",
     "linked_icd10": "P59.9", "speciality": "Pediatrics",
     "ceiling_inr": 7500, "pre_auth_required": True,
     "mandatory_investigations": ["Serum bilirubin (total/direct)"]},
    {"package_code": "MED_ANEMIA_D509", "package_name": "Iron-Deficiency Anemia Management",
     "linked_icd10": "D50.9", "speciality": "General Medicine",
     "ceiling_inr": 3000, "pre_auth_required": False,
     "mandatory_investigations": ["CBC", "Serum ferritin"]},
]

# ---------------------------------------------------------------------------
# Dataset C: Synthetic Rural Clinical Encounters (Ground-Truth Benchmark)
# ---------------------------------------------------------------------------
BENCHMARK_CASES = [
    {
        "case_id": "CASE_001",
        "raw_narrative": "Patient presents with high fever for 3 days, severe joint pain and a rash on the arms. No cough, no diarrhea.",
        "expected_chief_complaints": ["high fever", "joint pain", "rash"],
        "expected_negatives": ["cough", "diarrhea"],
        "gt_icd10": "A90", "gt_snomed": "38362002",
        "gt_package_code": "MED_INF_A90", "gt_payout_limit_inr": 8500,
    },
    {
        "case_id": "CASE_002",
        "raw_narrative": "Loose motions since yesterday, watery stools, mild stomach cramps. Patient denies blood in stool.",
        "expected_chief_complaints": ["loose motions", "watery stools", "stomach cramps"],
        "expected_negatives": ["blood in stool"],
        "gt_icd10": "A09", "gt_snomed": "25374005",
        "gt_package_code": "MED_INF_A09", "gt_payout_limit_inr": 4500,
    },
    {
        "case_id": "CASE_003",
        "raw_narrative": "Fever with cough and chest pain for 5 days, patient also reports mild breathlessness.",
        "expected_chief_complaints": ["fever", "cough", "chest pain", "breathlessness"],
        "expected_negatives": [],
        "gt_icd10": "J15.9", "gt_snomed": "53084003",
        "gt_package_code": "MED_PNEUMONIA_J15", "gt_payout_limit_inr": 15000,
    },
    {
        "case_id": "CASE_004",
        "raw_narrative": "Patient has fever, but no diarrhea or vomiting. Complains of chills and sweating episodes every alternate day.",
        "expected_chief_complaints": ["fever", "chills", "sweating"],
        "expected_negatives": ["diarrhea", "vomiting"],
        "gt_icd10": "B54", "gt_snomed": "61462000",
        "gt_package_code": "MED_INF_B54", "gt_payout_limit_inr": 6000,
    },
    {
        "case_id": "CASE_005",
        "raw_narrative": "sugar problm since 2 yrs, freqent urination n wt loss, no chest pain",
        "expected_chief_complaints": ["frequent urination", "weight loss"],
        "expected_negatives": ["chest pain"],
        "gt_icd10": "E11.9", "gt_snomed": "44054006",
        "gt_package_code": "MED_CHR_E119", "gt_payout_limit_inr": 6000,
    },
    {
        "case_id": "CASE_006",
        "raw_narrative": "Newborn, 3 days old, yellowish discoloration of skin and eyes noticed since morning.",
        "expected_chief_complaints": ["yellow skin", "yellow eyes"],
        "expected_negatives": [],
        "gt_icd10": "P59.9", "gt_snomed": "13835006",
        "gt_package_code": "PED_JAUNDICE_P599", "gt_payout_limit_inr": 7500,
    },
    {
        "case_id": "CASE_007",
        "raw_narrative": "BP high on three readings this week, occasional headache, denies chest pain or breathlessness.",
        "expected_chief_complaints": ["high blood pressure", "headache"],
        "expected_negatives": ["chest pain", "breathlessness"],
        "gt_icd10": "I10", "gt_snomed": "38341003",
        "gt_package_code": "MED_CHR_I10", "gt_payout_limit_inr": 4000,
    },
    {
        "case_id": "CASE_008",
        "raw_narrative": "Chronic cough for 6 weeks with evening weight loss and drenching night sweats.",
        "expected_chief_complaints": ["chronic cough", "weight loss", "night sweats"],
        "expected_negatives": [],
        "gt_icd10": "A15.0", "gt_snomed": "154283005",
        "gt_package_code": "MED_INF_A150", "gt_payout_limit_inr": 12000,
    },
]

def main():
    with open(os.path.join(OUT_DIR, "master_icd10_registry.json"), "w") as f:
        json.dump(ICD10_REGISTRY, f, indent=2)
    with open(os.path.join(OUT_DIR, "master_pmjay_tariffs.json"), "w") as f:
        json.dump(PMJAY_TARIFFS, f, indent=2)
    with open(os.path.join(OUT_DIR, "benchmark_ground_truth.json"), "w") as f:
        json.dump(BENCHMARK_CASES, f, indent=2)
    print(f"Wrote {len(ICD10_REGISTRY)} ICD-10 entries, "
          f"{len(PMJAY_TARIFFS)} PM-JAY packages, "
          f"{len(BENCHMARK_CASES)} benchmark cases.")

if __name__ == "__main__":
    main()
