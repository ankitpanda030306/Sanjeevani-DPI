"""
Tariff Matching Engine.

Deterministic lookup: given an ICD-10 code, find the PM-JAY benefit
package(s) linked to it and return the approved reimbursement ceiling and
pre-authorization requirement. No inference/model involved - this stage is
a pure dictionary join so the payout figure can never drift from the
official rate book.
"""

import json
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TariffMatch:
    package_code: str
    package_name: str
    speciality: str
    ceiling_inr: float
    pre_auth_required: bool
    mandatory_investigations: List[str]


class TariffMatcher:
    def __init__(self, tariffs_path: str):
        with open(tariffs_path, "r") as f:
            tariffs: List[dict] = json.load(f)
        # Index by ICD-10 code for O(1) lookup. A code could map to more
        # than one package in a fuller dataset, so keep it as a list.
        self._by_icd10 = {}
        for t in tariffs:
            self._by_icd10.setdefault(t["linked_icd10"], []).append(t)

    def match(self, icd10_code: str) -> Optional[TariffMatch]:
        """Return the primary (first-listed) package for an ICD-10 code."""
        candidates = self._by_icd10.get(icd10_code)
        if not candidates:
            return None
        t = candidates[0]
        return TariffMatch(
            package_code=t["package_code"],
            package_name=t["package_name"],
            speciality=t["speciality"],
            ceiling_inr=t["ceiling_inr"],
            pre_auth_required=t["pre_auth_required"],
            mandatory_investigations=t["mandatory_investigations"],
        )

    def match_all(self, icd10_code: str) -> List[TariffMatch]:
        candidates = self._by_icd10.get(icd10_code, [])
        return [
            TariffMatch(
                package_code=t["package_code"], package_name=t["package_name"],
                speciality=t["speciality"], ceiling_inr=t["ceiling_inr"],
                pre_auth_required=t["pre_auth_required"],
                mandatory_investigations=t["mandatory_investigations"],
            )
            for t in candidates
        ]


if __name__ == "__main__":
    matcher = TariffMatcher("data/master_pmjay_tariffs.json")
    print(matcher.match("A90"))
    print(matcher.match("Z99.9"))  # no match -> None
