from agents.repository_explorer import RepositoryExplorer


class TestFindDependentsAgnosticism:

    def test_finds_dependents_in_plain_javascript_files(self, tmp_path):
        # Regression test: the old implementation only scanned
        # .cs/.ts/.tsx, so a pure-JS React app (.js/.jsx, no TypeScript)
        # would never show up as a dependent of anything.
        (tmp_path / "UserService.js").write_text("export class UserService {}")
        (tmp_path / "UserCard.jsx").write_text(
            "import { UserService } from './UserService';"
        )

        dependents = RepositoryExplorer().find_dependents(
            str(tmp_path), "UserService.js"
        )

        assert "UserCard.jsx" in dependents

    def test_finds_dependents_in_python_files(self, tmp_path):
        (tmp_path / "user_service.py").write_text("class UserService: ...")
        (tmp_path / "handler.py").write_text("from user_service import UserService")

        dependents = RepositoryExplorer().find_dependents(
            str(tmp_path), "user_service.py"
        )

        assert "handler.py" in dependents

    def test_still_finds_dependents_in_dotnet_and_typescript(self, tmp_path):
        (tmp_path / "UserService.cs").write_text("public class UserService {}")
        (tmp_path / "UserController.cs").write_text(
            "public class UserController { private UserService _svc; }"
        )

        dependents = RepositoryExplorer().find_dependents(
            str(tmp_path), "UserService.cs"
        )

        assert "UserController.cs" in dependents

    def test_tsx_extension_is_stripped_correctly(self, tmp_path):
        # Regression test: the old code did
        # filename.replace(".cs","").replace(".ts","").replace(".tsx","")
        # -- for "Component.tsx" this replaced ".ts" BEFORE ".tsx" ever
        # matched, corrupting the target name to "Componentx".
        (tmp_path / "Component.tsx").write_text("export function Component() {}")
        (tmp_path / "Consumer.tsx").write_text(
            "import { Component } from './Component';"
        )

        dependents = RepositoryExplorer().find_dependents(
            str(tmp_path), "Component.tsx"
        )

        assert "Consumer.tsx" in dependents

    def test_skips_node_modules_directory(self, tmp_path):
        vendored = tmp_path / "node_modules" / "some-lib"
        vendored.mkdir(parents=True)
        (vendored / "index.js").write_text("UserService")
        (tmp_path / "UserService.js").write_text("export class UserService {}")

        dependents = RepositoryExplorer().find_dependents(
            str(tmp_path), "UserService.js"
        )

        assert dependents == []

    def test_skips_binary_files_without_raising(self, tmp_path):
        (tmp_path / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\nUserService")
        (tmp_path / "UserService.py").write_text("class UserService: ...")

        dependents = RepositoryExplorer().find_dependents(
            str(tmp_path), "UserService.py"
        )

        assert dependents == []

    def test_never_raises_on_unreadable_or_odd_files(self, tmp_path):
        (tmp_path / "weird_file").write_bytes(b"\xff\xfe\x00\x01UserService")
        (tmp_path / "UserService.go").write_text("package main")

        dependents = RepositoryExplorer().find_dependents(
            str(tmp_path), "UserService.go"
        )

        assert isinstance(dependents, list)
