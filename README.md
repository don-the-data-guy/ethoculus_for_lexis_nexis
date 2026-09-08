# Ethoculus for LexisNexis

**Behavioral experimentation for AI-powered legal research.**

Ethoculus for LexisNexis is an experimental framework for
running controlled, reproducible behavioral tests against
authorized LexisNexis APIs.

The project is designed to investigate questions such as:

- Does irrelevant authority change a legal conclusion?
- Does repetition change a legal conclusion?
- Does apparent expert consensus affect rule application?
- Does outcome pressure affect a legal answer?
- Are results stable across repeated trials?
- Are citations and authorities preserved across treatments?
- Does reasserting controlling authority restore a changed result?

## Scientific Boundary

Ethoculus measures observable model behavior.

It does not claim access to private chain-of-thought,
hidden model reasoning, consciousness, intent, weights,
or hidden activations.

## LexisNexis Integration

The adapter is intentionally API-contract driven.

LexisNexis endpoint paths, OAuth settings, request fields,
and response fields must be configured using documentation
provided through the authorized LexisNexis Developer Portal.

No credentials or licensed LexisNexis content should be
committed to this public repository.

## Dry Run

```bash
python run_experiment.py experiments/lexis_001.yaml --dry-run
