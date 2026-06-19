from pathlib import Path


DOC_ROOT = Path(__file__).resolve().parent.parent
CORE_DOCS = [
    DOC_ROOT / "README.md",
    DOC_ROOT / "docs" / "project_direction.md",
    DOC_ROOT / "docs" / "business_capability_model.md",
]
FORBIDDEN_TERMS = (
    "FY2026",
    "2026年度目標",
    "今年度目標",
    "今年度の目標",
    "annual goal",
    "goal-setting",
)
REQUIRED_CONCEPT_PAIRS = (
    "業務能力モデル（BusinessCapabilityModel）",
    "業務ルール（BusinessRule）",
    "判断基準（DecisionCriterion）",
    "実行可能タスク候補（ExecutableTaskCandidate）",
)
MIN_LINE_COUNTS = {
    DOC_ROOT / "README.md": 20,
    DOC_ROOT / "docs" / "project_direction.md": 10,
    DOC_ROOT / "docs" / "business_capability_model.md": 20,
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read_text(path).splitlines())


def _design_docs() -> list[Path]:
    design_docs = DOC_ROOT / "design" / "docs"
    if not design_docs.exists():
        return []
    return sorted(design_docs.rglob("*.md"))


def test_core_documents_exist() -> None:
    for path in CORE_DOCS:
        assert path.exists(), f"documentation file is missing: {path}"


def test_forbidden_annual_goal_terms_are_absent() -> None:
    targets = [*CORE_DOCS, *_design_docs()]
    for path in targets:
        content = _read_text(path)
        for term in FORBIDDEN_TERMS:
            assert term not in content, f"forbidden term {term!r} found in {path}"


def test_required_concept_pairs_exist_across_core_docs() -> None:
    combined = "\n".join(_read_text(path) for path in CORE_DOCS)
    for term in REQUIRED_CONCEPT_PAIRS:
        assert term in combined, f"required concept pair is missing: {term}"


def test_core_markdown_files_have_readable_line_counts() -> None:
    for path, minimum in MIN_LINE_COUNTS.items():
        assert _line_count(path) >= minimum, f"{path} should have at least {minimum} lines"
