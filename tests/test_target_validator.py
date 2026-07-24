from agents.target_validator import TargetValidator


class TestTargetValidatorExistsInTarget:

    def test_never_raises_on_malformed_endpoint_item(self):
        validator = TargetValidator(repo_path="/unused")

        result = validator._exists_in_target("endpoint no colon", "content")

        assert result is False

    def test_never_raises_on_malformed_dependency_item(self):
        validator = TargetValidator(repo_path="/unused")

        result = validator._exists_in_target("dependência no colon", "content")

        assert result is False

    def test_detects_existing_endpoint(self):
        validator = TargetValidator(repo_path="/unused")

        result = validator._exists_in_target(
            "Novo endpoint GET: /users", "route is /users here"
        )

        assert result is True

    def test_detects_existing_dependency(self):
        validator = TargetValidator(repo_path="/unused")

        result = validator._exists_in_target(
            "Nova dependência: System.Text.Json", "uses Json somewhere"
        )

        assert result is True

    def test_unrecognized_item_shape_returns_false(self):
        validator = TargetValidator(repo_path="/unused")

        result = validator._exists_in_target("Nova propriedade: Name", "Name here")

        assert result is False

    def test_validate_is_technology_agnostic_across_stacks(self, tech_stack):
        from agents.change_summarizer import ChangeSummarizer
        from tests.conftest import diff_lines

        summary = ChangeSummarizer().summarize(
            {"additions": diff_lines(tech_stack), "removals": []}
        )

        validator = TargetValidator(repo_path="/unused")
        results = validator.validate("target_ref", "file.ext", summary)

        assert len(results) == len(summary)
        for result in results:
            assert set(result.keys()) == {"item", "already_exists"}
            assert isinstance(result["already_exists"], bool)
