"""
Stage 5: Strict Schema Validation.

Validates the final pipeline output against a simplified ABDM FHIR
OPConsult-style structure before it's allowed downstream. Written as a
dependency-free validator (dataclasses + manual checks) so it runs without
network access; drop-in swap for `pydantic.BaseModel` + `field_validator`
once that package is available in your environment.
"""

from dataclasses import dataclass, field
from typing import List, Optional


class SchemaValidationError(Exception):
    pass


@dataclass
class OPConsultPayload:
    case_id: str
    chief_complaints: List[str]
    icd10_code: str
    snomed_id: str
    confidence: float
    package_code: Optional[str]
    ceiling_inr: Optional[float]
    pre_auth_required: Optional[bool]

    def validate(self) -> None:
        errors = []
        if not self.case_id:
            errors.append("case_id is required")
        if not isinstance(self.chief_complaints, list) or not self.chief_complaints:
            errors.append("chief_complaints must be a non-empty list")
        if not self.icd10_code or not _looks_like_icd10(self.icd10_code):
            errors.append(f"icd10_code '{self.icd10_code}' is not a valid ICD-10-CM format")
        if not self.snomed_id or not self.snomed_id.isdigit():
            errors.append(f"snomed_id '{self.snomed_id}' must be a numeric SNOMED concept id")
        if not (0.0 <= self.confidence <= 1.0):
            errors.append("confidence must be between 0 and 1")
        if self.package_code is not None and self.ceiling_inr is None:
            errors.append("ceiling_inr required when package_code is present")
        if errors:
            raise SchemaValidationError("; ".join(errors))


def _looks_like_icd10(code: str) -> bool:
    # e.g. A09, J15.9, E11.9, I10 - letter + 2 digits, optional .digit(s)
    if len(code) < 3:
        return False
    if not code[0].isalpha():
        return False
    rest = code[1:]
    main, _, decimal = rest.partition(".")
    if not main.isdigit():
        return False
    if decimal and not decimal.isdigit():
        return False
    return True


if __name__ == "__main__":
    ok = OPConsultPayload(
        case_id="CASE_001", chief_complaints=["high fever", "joint pain"],
        icd10_code="A90", snomed_id="38362002", confidence=0.87,
        package_code="MED_INF_A90", ceiling_inr=8500, pre_auth_required=False,
    )
    ok.validate()
    print("Valid payload OK")

    try:
        bad = OPConsultPayload(
            case_id="", chief_complaints=[], icd10_code="XYZ",
            snomed_id="abc", confidence=1.5,
            package_code="P1", ceiling_inr=None, pre_auth_required=True,
        )
        bad.validate()
    except SchemaValidationError as e:
        print("Correctly rejected invalid payload:", e)
