"""
evaluate_accuracy.py

Runs the full pipeline against the curated ground-truth benchmark cases and
reports the metrics called for in the spec:

  - Entity Extraction F1-score
  - Diagnostic Code Exact Match (target >= 95%)
  - Negative Mention Handling (target 100%)
  - Schema Conformance Rate (target 100%)
  - Tariff Calculation Precision (target 100%)

Usage:
    python evaluate_accuracy.py
"""

import json
import os
import time

from pipeline import ClinicalCodingPipeline

HERE = os.path.dirname(os.path.abspath(__file__))
GROUND_TRUTH_PATH = os.path.join(HERE, "data", "benchmark_ground_truth.json")


def _tokenize(phrases):
    """Turn a list of phrases into a flat set of tokens for loose F1 scoring."""
    tokens = set()
    for p in phrases:
        tokens.update(p.lower().split())
    return tokens


def entity_f1(expected, predicted):
    exp_tokens = _tokenize(expected)
    pred_tokens = _tokenize(predicted)
    if not exp_tokens and not pred_tokens:
        return 1.0
    if not pred_tokens or not exp_tokens:
        return 0.0
    tp = len(exp_tokens & pred_tokens)
    precision = tp / len(pred_tokens)
    recall = tp / len(exp_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def run_benchmark():
    with open(GROUND_TRUTH_PATH, "r") as f:
        cases = json.load(f)

    pipeline = ClinicalCodingPipeline()
    print(f"Embedding backend in use: {pipeline.retriever.embedder.name}\n")

    results = []
    total_latency = 0.0

    for case in cases:
        t0 = time.perf_counter()
        result = pipeline.run(case["case_id"], case["raw_narrative"])
        latency = time.perf_counter() - t0
        total_latency += latency

        predicted_icd10 = result.best_match.icd10_code if result.best_match else None
        exact_match = predicted_icd10 == case["gt_icd10"]

        # Negative mention handling: none of the expected negatives should
        # have leaked into the active complaint list.
        active_lower = " ".join(result.active_complaints).lower()
        negatives_leaked = [
            neg for neg in case.get("expected_negatives", [])
            if neg.lower() in active_lower
        ]
        negative_handling_ok = len(negatives_leaked) == 0

        f1 = entity_f1(case["expected_chief_complaints"], result.active_complaints)

        tariff_ok = (
            result.tariff is not None
            and result.tariff.package_code == case["gt_package_code"]
            and result.tariff.ceiling_inr == case["gt_payout_limit_inr"]
        )

        results.append({
            "case_id": case["case_id"],
            "predicted_icd10": predicted_icd10,
            "gt_icd10": case["gt_icd10"],
            "exact_match": exact_match,
            "confidence": result.best_match.confidence if result.best_match else 0.0,
            "entity_f1": round(f1, 3),
            "negatives_leaked": negatives_leaked,
            "negative_handling_ok": negative_handling_ok,
            "schema_valid": result.schema_valid,
            "schema_error": result.schema_error,
            "tariff_ok": tariff_ok,
            "predicted_package": result.tariff.package_code if result.tariff else None,
            "latency_sec": round(latency, 4),
        })

    n = len(results)
    exact_match_rate = sum(r["exact_match"] for r in results) / n
    avg_f1 = sum(r["entity_f1"] for r in results) / n
    negative_handling_rate = sum(r["negative_handling_ok"] for r in results) / n
    schema_conformance_rate = sum(r["schema_valid"] for r in results) / n
    tariff_precision = sum(r["tariff_ok"] for r in results) / n
    avg_latency = total_latency / n

    print("=" * 72)
    print("PER-CASE RESULTS")
    print("=" * 72)
    for r in results:
        status = "PASS" if r["exact_match"] else "FAIL"
        print(f"[{status}] {r['case_id']}: predicted={r['predicted_icd10']} "
              f"expected={r['gt_icd10']} conf={r['confidence']:.3f} "
              f"F1={r['entity_f1']} negatives_leaked={r['negatives_leaked']} "
              f"schema_valid={r['schema_valid']} tariff_ok={r['tariff_ok']}")

    print("\n" + "=" * 72)
    print("ACCURACY SCORECARD")
    print("=" * 72)
    print(f"Entity Extraction F1-Score        : {avg_f1:.2%}")
    print(f"Diagnostic Code Exact Match (EM)   : {exact_match_rate:.2%}  (target >= 95%)")
    print(f"Negative Mention Handling          : {negative_handling_rate:.2%}  (target 100%)")
    print(f"Schema Conformance Rate            : {schema_conformance_rate:.2%}  (target 100%)")
    print(f"Tariff Calculation Precision       : {tariff_precision:.2%}  (target 100%)")
    print(f"Average latency per case           : {avg_latency*1000:.1f} ms")
    print("=" * 72)

    return {
        "n_cases": n,
        "entity_f1": avg_f1,
        "exact_match_rate": exact_match_rate,
        "negative_handling_rate": negative_handling_rate,
        "schema_conformance_rate": schema_conformance_rate,
        "tariff_precision": tariff_precision,
        "avg_latency_sec": avg_latency,
        "per_case": results,
    }


if __name__ == "__main__":
    summary = run_benchmark()
    out_path = os.path.join(HERE, "accuracy_report.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=float)
    print(f"\nFull report written to {out_path}")
