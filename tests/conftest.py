"""
Shared fixtures for the test suite.

TECH_SAMPLES holds representative "added lines" for a few different
technology stacks. The deterministic analysis pipeline (change_summarizer,
change_inspector, conflict_detector, target_validator, ...) was originally
written against .NET/C# conventions (using statements, app.MapGet, public
properties). It should never crash for other stacks, even when it can't
extract any semantic meaning from them -- an empty result is fine, an
exception is not. Tests in test_technology_agnostic.py run every stack
through the same functions and assert on that contract.
"""

import pytest


TECH_SAMPLES = {
    "dotnet": [
        "using System.Text.Json;",
        "public string Name { get; set; }",
        'app.MapGet("/users/{id}", GetUserAsync);',
        'app.MapPost("/users", CreateUserAsync);',
        "public async Task<User> GetUserAsync(int id)",
        "private void Validate(User user)",
        "class UserService",
        "interface IUserRepository",
    ],
    "react": [
        'import { useState } from "react";',
        "export function UserCard({ user }: { user: User }) {",
        "  const [isOpen, setIsOpen] = useState(false);",
        "interface UserCardProps {",
        "  user: User;",
        "export class UserCard extends React.Component<UserCardProps> {",
        "  render() {",
        '    return <div className="card">{this.props.user.name}</div>;',
    ],
    "python": [
        "import requests",
        "class UserService:",
        "    def get_user(self, user_id: int) -> dict:",
        '        return self.session.get(f"/users/{user_id}").json()',
        "    async def create_user(self, payload: dict) -> dict:",
    ],
}


def diff_lines(stack: str, prefix: str = "+") -> list[str]:
    return [f"{prefix}{line}" for line in TECH_SAMPLES[stack]]


@pytest.fixture(params=sorted(TECH_SAMPLES.keys()))
def tech_stack(request) -> str:
    return request.param


@pytest.fixture
def change_result_factory():
    def _build(stack: str) -> dict:
        return {
            "file": f"sample.{stack}",
            "additions": diff_lines(stack, prefix="+"),
            "removals": [],
            "total_additions": len(TECH_SAMPLES[stack]),
            "total_removals": 0,
        }

    return _build
