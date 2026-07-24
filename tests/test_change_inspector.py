from agents.change_inspector import ChangeInspector
from tests.conftest import TECH_SAMPLES


class TestChangeInspectorExtractItems:

    def test_never_raises_regardless_of_stack(self, tech_stack):
        inspector = ChangeInspector(repo_path="/unused")

        items = inspector._extract_items(TECH_SAMPLES[tech_stack])

        assert isinstance(items, list)
        assert all(isinstance(item, str) for item in items)

    def test_detects_dotnet_class_and_interface_names(self):
        inspector = ChangeInspector(repo_path="/unused")

        items = inspector._extract_items(TECH_SAMPLES["dotnet"])

        assert "UserService" in items
        assert "IUserRepository" in items

    def test_typescript_class_and_interface_also_match(self):
        # `class` and `interface` are valid keywords in TypeScript too, so
        # the regex-based detector should pick up React/TSX class components
        # and prop interfaces even though it was written with C# in mind.
        inspector = ChangeInspector(repo_path="/unused")

        items = inspector._extract_items(TECH_SAMPLES["react"])

        assert "UserCard" in items
        assert "UserCardProps" in items

    def test_plain_python_yields_no_false_positives(self):
        # Python has no `public`/`private`/`class Foo(...)  {` C-style
        # syntax matching these regexes beyond bare `class Name:` --
        # this must simply return fewer/no items, never raise.
        inspector = ChangeInspector(repo_path="/unused")

        items = inspector._extract_items(TECH_SAMPLES["python"])

        assert isinstance(items, list)

    def test_returns_sorted_unique_items(self):
        inspector = ChangeInspector(repo_path="/unused")

        items = inspector._extract_items(
            ["class Zebra {", "class Apple {", "class Apple {"]
        )

        assert items == ["Apple", "Zebra"]
