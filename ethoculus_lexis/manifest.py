from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Condition:
    name: str
    prompt: str


@dataclass
class Case:
    case_id: str
    expected: str
    conditions: list[Condition]


@dataclass
class Experiment:
    experiment_id: str
    title: str
    trials: int
    cases: list[Case]


def load_manifest(path: str | Path) -> Experiment:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        raw: dict[str, Any] = yaml.safe_load(f)

    cases = []

    for case_data in raw["cases"]:
        conditions = [
            Condition(
                name=item["name"],
                prompt=item["prompt"],
            )
            for item in case_data["conditions"]
        ]

        cases.append(
            Case(
                case_id=case_data["case_id"],
                expected=str(case_data["expected"]),
                conditions=conditions,
            )
        )

    return Experiment(
        experiment_id=raw["experiment_id"],
        title=raw["title"],
        trials=int(raw.get("trials", 1)),
        cases=cases,
    )
