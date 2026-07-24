from agents.conflict_detector import ConflictDetector


VALID_STATUSES = {"APPLY", "ALREADY_EXISTS", "CONFLICT", "UNKNOWN"}


class TestConflictDetectorClassify:

    def test_never_raises_on_malformed_endpoint_item(self):
        # Regression test: _analyze_endpoint used to do
        # item.split(":", maxsplit=1)[1] unconditionally, raising
        # IndexError for any "endpoint" item without a colon.
        detector = ConflictDetector(repo_path="/unused")

        status = detector._classify("endpoint without a colon", "some content")

        assert status in VALID_STATUSES

    def test_well_formed_endpoint_item_still_works(self):
        detector = ConflictDetector(repo_path="/unused")

        status = detector._classify(
            "Novo endpoint GET: /users/{id}", "no matching route here"
        )

        assert status == "APPLY"

    def test_endpoint_already_present_in_target(self):
        detector = ConflictDetector(repo_path="/unused")

        status = detector._classify(
            "Novo endpoint GET: /users/{id}",
            'app.MapGet("/users/{id}", GetUser);',
        )

        assert status == "ALREADY_EXISTS"

    def test_never_raises_on_malformed_property_item(self):
        detector = ConflictDetector(repo_path="/unused")

        status = detector._classify("Nova propriedade:", "")

        assert status in VALID_STATUSES

    def test_never_raises_on_malformed_dependency_item(self):
        detector = ConflictDetector(repo_path="/unused")

        status = detector._classify("Nova dependência:", "")

        assert status in VALID_STATUSES

    def test_never_raises_on_malformed_method_item(self):
        detector = ConflictDetector(repo_path="/unused")

        status = detector._classify("Novo método: (", "")

        assert status in VALID_STATUSES

    def test_unknown_item_shape_returns_unknown(self):
        detector = ConflictDetector(repo_path="/unused")

        status = detector._classify("something we've never seen before", "content")

        assert status == "UNKNOWN"

    def test_analyze_is_technology_agnostic_across_stacks(self, tech_stack):
        # Whatever ChangeSummarizer produced for a given stack, analyze()
        # must always return one well-shaped result per item, never raise.
        from agents.change_summarizer import ChangeSummarizer
        from tests.conftest import diff_lines

        summary = ChangeSummarizer().summarize(
            {"additions": diff_lines(tech_stack), "removals": []}
        )

        detector = ConflictDetector(repo_path="/unused")
        results = detector.analyze("target_ref", "file.ext", summary)

        assert len(results) == len(summary)
        for result in results:
            assert set(result.keys()) == {"item", "status"}
            assert result["status"] in VALID_STATUSES
