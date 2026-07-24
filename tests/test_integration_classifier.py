import json

from classifiers.integration_classifier import IntegrationClassifier


def write_metadata(tmp_path, commits, files_changed, age_days):
    metadata = {
        "source": "feature",
        "target": "qa",
        "commits": commits,
        "files_changed": files_changed,
        "age_days": age_days,
    }
    (tmp_path / "metadata.json").write_text(json.dumps(metadata))
    return tmp_path


class TestIntegrationClassifier:

    def test_small_change_classified_as_strategy_a(self, tmp_path):
        write_metadata(tmp_path, commits=5, files_changed=10, age_days=5)

        result = IntegrationClassifier().classify(str(tmp_path))

        assert result["strategy"] == "A"
        assert result["confidence"] > 0

    def test_old_branch_forces_strategy_d(self, tmp_path):
        # commits/files_changed deliberately fall outside every other
        # bucket (not <=10/20, not <=30/50, not <=50/100, not >100) so
        # only the age_days>90 rule is in play.
        write_metadata(tmp_path, commits=60, files_changed=60, age_days=200)

        result = IntegrationClassifier().classify(str(tmp_path))

        assert result["strategy"] == "D"

    def test_large_file_count_forces_strategy_d(self, tmp_path):
        write_metadata(tmp_path, commits=5, files_changed=150, age_days=1)

        result = IntegrationClassifier().classify(str(tmp_path))

        assert result["strategy"] == "D"

    def test_writes_classification_file(self, tmp_path):
        write_metadata(tmp_path, commits=5, files_changed=10, age_days=5)

        IntegrationClassifier().classify(str(tmp_path))

        assert (tmp_path / "classification.json").exists()

    def test_classification_is_technology_agnostic(self, tmp_path):
        # The classifier only reasons about commit/file counts and age --
        # it must produce the exact same shape no matter which stack the
        # repository is written in.
        write_metadata(tmp_path, commits=5, files_changed=10, age_days=5)

        result = IntegrationClassifier().classify(str(tmp_path))

        assert set(result.keys()) == {
            "source", "target", "strategy", "confidence", "reasons"
        }
        assert isinstance(result["reasons"], list)
