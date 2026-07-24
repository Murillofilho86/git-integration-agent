from agents.integration_scope_builder import IntegrationScopeBuilder


class TestCategorize:

    def test_dotnet_clean_architecture_layers_are_recognized(self):
        builder = IntegrationScopeBuilder(repo_path="/unused")

        categories = builder.categorize(
            [
                "Project.Api/Controllers/UserController.cs",
                "Project.Application/Services/UserService.cs",
                "Project.Domain/Entities/User.cs",
                "Project.Infrastructure/Repositories/UserRepository.cs",
                "test/UserServiceTests.cs",
            ]
        )

        assert categories["Api"] == ["Project.Api/Controllers/UserController.cs"]
        assert categories["Application"] == [
            "Project.Application/Services/UserService.cs"
        ]
        assert categories["Domain"] == ["Project.Domain/Entities/User.cs"]
        assert categories["Infrastructure"] == [
            "Project.Infrastructure/Repositories/UserRepository.cs"
        ]
        assert categories["Tests"] == ["test/UserServiceTests.cs"]

    def test_react_files_fall_back_to_other_without_raising(self):
        # The category taxonomy is .NET Clean Architecture-shaped
        # (.Api/, .Application/, .Domain/, .Infrastructure/) and doesn't
        # know React project layouts -- that's fine as long as it never
        # raises and simply buckets everything into "Other".
        builder = IntegrationScopeBuilder(repo_path="/unused")

        categories = builder.categorize(
            [
                "src/components/UserCard.tsx",
                "src/pages/UserPage.tsx",
                "src/hooks/useUser.ts",
            ]
        )

        assert categories["Other"] == [
            "src/components/UserCard.tsx",
            "src/pages/UserPage.tsx",
            "src/hooks/useUser.ts",
        ]
        assert categories["Api"] == []

    def test_categorize_never_raises_and_always_returns_all_buckets(self, tech_stack):
        builder = IntegrationScopeBuilder(repo_path="/unused")

        categories = builder.categorize([f"some/path/file.{tech_stack}"])

        assert set(categories.keys()) == {
            "Api", "Application", "Domain", "Infrastructure", "Tests", "Other"
        }


class TestConsolidateScope:

    def test_counts_shared_files_across_dependencies(self):
        builder = IntegrationScopeBuilder(repo_path="/unused")

        scope = [
            {"dependency": "A", "files": ["shared.py", "only_a.py"]},
            {"dependency": "B", "files": ["shared.py", "only_b.py"]},
        ]

        result = builder.consolidate_scope(scope)

        assert result["total_unique"] == 3
        assert result["shared_files"] == ["shared.py"]

    def test_handles_empty_scope(self):
        builder = IntegrationScopeBuilder(repo_path="/unused")

        result = builder.consolidate_scope([])

        assert result["total_unique"] == 0
        assert result["shared_files"] == []
