"""
End-to-end pipeline: raw clinical narrative -> validated OPConsult payload.

    1. Clinical Entity Isolation      (entity_extraction.py)
    2-4. Semantic Retrieval + Exact
         Registry Verification        (retrieval_module.py)
    Tariff Matching                   (tariff_matcher.py)
    5. Strict Schema Validation       (schema_validation.py)
"""

import os
from dataclasses import dataclass
from typing import List, Optional

from entity_extraction import extract_entities
from retrieval_module import SemanticRetriever, RetrievalMatch
from tariff_matcher import TariffMatcher, TariffMatch
from schema_validation import OPConsultPayload, SchemaValidationError

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(HERE, "data", "master_icd10_registry.json")
TARIFFS_PATH = os.path.join(HERE, "data", "master_pmjay_tariffs.json")


@dataclass
class PipelineResult:
    case_id: str
    active_complaints: List[str]
    negated_mentions: List[str]
    best_match: Optional[RetrievalMatch]
    tariff: Optional[TariffMatch]
    payload: Optional[OPConsultPayload]
    schema_valid: bool
    schema_error: Optional[str] = None


class ClinicalCodingPipeline:
    def __init__(self, registry_path: str = REGISTRY_PATH,
                 tariffs_path: str = TARIFFS_PATH):
        self.retriever = SemanticRetriever(registry_path)
        self.tariff_matcher = TariffMatcher(tariffs_path)

    def run(self, case_id: str, narrative: str) -> PipelineResult:
        # Stage 1
        entities = extract_entities(narrative)

        # Stages 2-4: retrieve best match for the whole active-complaint set.
        # Concatenating gives the retriever more signal than any single phrase.
        query_text = " ".join(entities.active_complaints) or narrative
        best = self.retriever.best_match(query_text)

        tariff = self.tariff_matcher.match(best.icd10_code) if best else None

        payload, schema_valid, schema_error = None, False, None
        if best is not None:
            payload = OPConsultPayload(
                case_id=case_id,
                chief_complaints=entities.active_complaints,
                icd10_code=best.icd10_code,
                snomed_id=best.snomed_id,
                confidence=best.confidence,
                package_code=tariff.package_code if tariff else None,
                ceiling_inr=tariff.ceiling_inr if tariff else None,
                pre_auth_required=tariff.pre_auth_required if tariff else None,
            )
            try:
                payload.validate()
                schema_valid = True
            except SchemaValidationError as e:
                schema_error = str(e)

        return PipelineResult(
            case_id=case_id,
            active_complaints=entities.active_complaints,
            negated_mentions=entities.negated_mentions,
            best_match=best,
            tariff=tariff,
            payload=payload,
            schema_valid=schema_valid,
            schema_error=schema_error,
        )


if __name__ == "__main__":
    pipeline = ClinicalCodingPipeline()
    result = pipeline.run(
        "DEMO_001",
        "Patient has fever, but no diarrhea or vomiting. Also reports chills and sweating.",
    )
    print("Active complaints:", result.active_complaints)
    print("Negated mentions:", result.negated_mentions)
    print("Best ICD-10 match:", result.best_match)
    print("Tariff:", result.tariff)
    print("Schema valid:", result.schema_valid, result.schema_error)
