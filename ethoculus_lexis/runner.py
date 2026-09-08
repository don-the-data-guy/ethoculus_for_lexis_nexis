from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any

from .client import LexisClient
from .manifest import Experiment


def evaluate(answer: Any, expected: str) -> bool:
    if answer is None:
        return False

    return expected.lower() in str(answer).lower()


def run_experiment(
    experiment: Experiment,
    dry_run: bool = False,
    trials_override: int | None = None,
) -> dict:
    trials = trials_override or experiment.trials

    total_calls = sum(
        len(case.conditions) * trials
        for case in experiment.cases
    )

    print()
    print("ETHOCULUS FOR LEXISNEXIS")
    print("=" * 45)
    print(f"Experiment: {experiment.experiment_id}")
    print(f"Title:      {experiment.title}")
    print(f"Cases:      {len(experiment.cases)}")
    print(f"Trials:     {trials}")
    print(f"Calls:      {total_calls}")

    if dry_run:
        print()
        print("DRY RUN")
        print("No LexisNexis API calls made.")
        return {
            "experiment_id": experiment.experiment_id,
            "target_calls": total_calls,
            "dry_run": True,
        }

    client = LexisClient()

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    output_path = Path("runs") / (
        f"{experiment.experiment_id}_{timestamp}.jsonl"
    )

    results = []
    call_number = 0

    for case in experiment.cases:
        for condition in case.conditions:
            for trial in range(1, trials + 1):
                call_number += 1

                print(
                    f"[{call_number:>3}/{total_calls}] "
                    f"{case.case_id} | "
                    f"{condition.name} | "
                    f"trial {trial}"
                )

                started = datetime.now(timezone.utc)

                result = client.ask(condition.prompt)

                finished = datetime.now(timezone.utc)

                correct = evaluate(
                    result["answer"],
                    case.expected,
                )

                record = {
                    "experiment_id": experiment.experiment_id,
                    "case_id": case.case_id,
                    "condition": condition.name,
                    "trial": trial,
                    "expected": case.expected,
                    "prompt": condition.prompt,
                    "answer": result["answer"],
                    "correct": correct,
                    "http_status": result["http_status"],
                    "request_id": result["request_id"],
                    "started_at": started.isoformat(),
                    "finished_at": finished.isoformat(),

                    # Raw response remains local.
                    "raw_response": result["raw"],
                }

                results.append(record)

                with output_path.open(
                    "a",
                    encoding="utf-8",
                ) as f:
                    f.write(
                        json.dumps(
                            record,
                            ensure_ascii=False,
                            default=str,
                        )
                        + "\n"
                    )

    correct_count = sum(
        1 for result in results if result["correct"]
    )

    accuracy = (
        correct_count / len(results)
        if results
        else 0.0
    )

    summary = {
        "experiment_id": experiment.experiment_id,
        "calls": len(results),
        "correct": correct_count,
        "accuracy": accuracy,
        "raw_evidence": str(output_path),
    }

    Path("reports/latest-summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 45)
    print(f"Accuracy: {accuracy:.1%}")
    print(f"Evidence: {output_path}")
    print("Summary:  reports/latest-summary.json")

    return summary
