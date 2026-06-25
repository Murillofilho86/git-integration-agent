from dataclasses import dataclass

@dataclass
class IntegrationAnalysis:
    source_ref: str
    target_ref: str

    commits_ahead: int
    files_changed: int
    age_days: int