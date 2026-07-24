from agents.change_summarizer import ChangeSummarizer


class TestChangeSummarizer:

    def test_never_raises_regardless_of_stack(self, tech_stack, change_result_factory):
        change_result = change_result_factory(tech_stack)

        summary = ChangeSummarizer().summarize(change_result)

        assert isinstance(summary, list)
        assert all(isinstance(item, str) for item in summary)

    def test_missing_keys_are_tolerated(self):
        # A caller that only has additions (no removals key at all) must
        # not crash the summarizer -- .get() defaults are relied upon.
        summary = ChangeSummarizer().summarize({"additions": []})

        assert summary == []

    def test_detects_dotnet_using_statement(self, change_result_factory):
        summary = ChangeSummarizer().summarize(change_result_factory("dotnet"))

        assert any("Nova dependência" in item for item in summary)

    def test_detects_dotnet_minimal_api_endpoints(self, change_result_factory):
        summary = ChangeSummarizer().summarize(change_result_factory("dotnet"))

        assert any("Novo endpoint GET" in item for item in summary)
        assert any("Novo endpoint POST" in item for item in summary)

    def test_react_content_yields_no_dotnet_false_positives(self, change_result_factory):
        # React/TS source has no `using` statements or app.MapX calls, so
        # the .NET-specific detectors must legitimately find nothing --
        # an empty list is correct here, not a bug.
        summary = ChangeSummarizer().summarize(change_result_factory("react"))

        assert not any("endpoint" in item.lower() for item in summary)
        assert not any("dependência" in item.lower() for item in summary)

    def test_deduplicates_repeated_items(self):
        change_result = {
            "additions": [
                "+using System;",
                "+using System;",
            ],
            "removals": [],
        }

        summary = ChangeSummarizer().summarize(change_result)

        assert summary.count("Nova dependência: System") == 1
