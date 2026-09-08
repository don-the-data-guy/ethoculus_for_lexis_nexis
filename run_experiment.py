import argparse

from ethoculus_lexis.manifest import load_manifest
from ethoculus_lexis.runner import run_experiment


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Run controlled Ethoculus experiments "
            "against LexisNexis APIs."
        )
    )

    parser.add_argument(
        "manifest",
        help="Path to experiment YAML manifest.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate experiment without API calls.",
    )

    parser.add_argument(
        "--trials",
        type=int,
        default=None,
        help="Override trials per condition.",
    )

    args = parser.parse_args()

    experiment = load_manifest(args.manifest)

    run_experiment(
        experiment,
        dry_run=args.dry_run,
        trials_override=args.trials,
    )


if __name__ == "__main__":
    main()
