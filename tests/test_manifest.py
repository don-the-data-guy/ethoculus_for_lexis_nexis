from ethoculus_lexis.manifest import load_manifest


def test_manifest_loads():
    experiment = load_manifest(
        "experiments/lexis_001.yaml"
    )

    assert experiment.experiment_id == "LEXIS-001"
    assert len(experiment.cases) == 1
    assert len(experiment.cases[0].conditions) == 6
