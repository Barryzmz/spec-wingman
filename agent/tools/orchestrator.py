from pathlib import Path

from tools.utils import validate_project_path
from tools.discover import swm_discover_context_tool
from tools.extract import swm_extract_context_tool
from tools.clarify import swm_clarify_context_tool
from tools.analyze import swm_analyze_context_tool
from tools.spec import swm_spec_context_tool
from tools.design import swm_design_context_tool
from tools.log import swm_log_context_tool

_REQUIRED_STEP1 = [
    "source-summary.md", "extracted-facts.md",
    "open-questions.md", "assumptions.md", "glossary.md",
]
_REQUIRED_STEP2 = [
    "product-vision.md", "functional-requirements.md", "business-rules.md",
    "data-requirements.md", "workflow-requirements.md", "permission-requirements.md",
    "non-functional-requirements.md", "user-roles.md",
]
_REQUIRED_STEP4 = [
    "use-cases.md", "user-stories.md", "acceptance-criteria.md",
    "domain-model.md", "state-transitions.md", "edge-cases.md",
]
_REQUIRED_STEP6 = [
    "system-design-brief.md", "api-draft.md", "database-draft.md",
    "frontend-pages.md", "test-cases.md", "development-tasks.md",
]


def _dir_complete(dir_path: Path, required: list[str]) -> bool:
    return dir_path.exists() and all((dir_path / f).exists() for f in required)


def _log_is_current(root: Path) -> bool:
    """Return True if changelog is newer than all specs files (excluding 05-versions)."""
    changelog = root / "specs" / "05-versions" / "changelog.md"
    if not changelog.exists():
        return False
    log_mtime = changelog.stat().st_mtime
    for step in ["01-discovery", "02-requirements", "03-analysis", "04-design-ready"]:
        d = root / "specs" / step
        if d.exists():
            for f in d.iterdir():
                if f.is_file() and f.stat().st_mtime > log_mtime:
                    return False
    return True


def _step3_state(specs: Path) -> str:
    """
    Returns one of: 'PHASE1_READY', 'WAITING', 'PHASE2_READY', 'DONE'

    answer-draft.md has content  → PHASE2_READY (user answered, backfill pending)
    answer-draft.md exists empty → DONE (Phase 2 complete, draft cleared)
    open-questions newer than requirements → WAITING (Phase 1 done, no answers yet)
    otherwise                    → PHASE1_READY
    """
    answer_draft = specs / "01-discovery" / "answer-draft.md"

    if answer_draft.exists():
        return "PHASE2_READY" if answer_draft.read_text(encoding="utf-8").strip() else "DONE"

    open_q = specs / "01-discovery" / "open-questions.md"
    if open_q.exists():
        req_dir = specs / "02-requirements"
        req_files = [f for f in req_dir.iterdir() if f.is_file()] if req_dir.exists() else []
        if req_files:
            newest_req = max(f.stat().st_mtime for f in req_files)
            if open_q.stat().st_mtime > newest_req:
                return "WAITING"

    return "PHASE1_READY"


def determine_state(project_path: str) -> str:
    root = validate_project_path(project_path)
    specs = root / "specs"

    # Step 0: inputs
    user_desc = specs / "00-inputs" / "user-description.md"
    if not user_desc.exists() or not user_desc.read_text(encoding="utf-8").strip():
        return "NOT_STARTED"

    # Step 1: Discovery
    if not _dir_complete(specs / "01-discovery", _REQUIRED_STEP1):
        return "STEP_1_READY"
    if not _log_is_current(root):
        return "LOG_READY"

    # Step 2: Requirements
    if not _dir_complete(specs / "02-requirements", _REQUIRED_STEP2):
        return "STEP_2_READY"
    if not _log_is_current(root):
        return "LOG_READY"

    # Step 3: Clarify — only enter if Step 4 analysis is not yet done
    if not _dir_complete(specs / "03-analysis", _REQUIRED_STEP4):
        s3 = _step3_state(specs)
        if s3 == "PHASE1_READY":
            return "STEP_3_PHASE1_READY"
        if s3 == "WAITING":
            if not _log_is_current(root):
                return "LOG_READY"
            return "STEP_3_WAITING"
        if s3 == "PHASE2_READY":
            return "STEP_3_PHASE2_READY"
        # s3 == "DONE": fall through to Step 4
        if not _log_is_current(root):
            return "LOG_READY"
        return "STEP_4_READY"

    if not _log_is_current(root):
        return "LOG_READY"

    # Step 5: Spec
    if not (specs / "04-design-ready" / "requirement-spec.md").exists():
        return "STEP_5_READY"
    if not _log_is_current(root):
        return "LOG_READY"

    # Step 6: Design
    if not _dir_complete(specs / "04-design-ready", _REQUIRED_STEP6):
        return "STEP_6_READY"
    if not _log_is_current(root):
        return "LOG_READY"

    return "COMPLETE"


def swm_next_tool(project_path: str) -> str:
    root = validate_project_path(project_path)
    state = determine_state(project_path)

    if state == "NOT_STARTED":
        return (
            "# SpecWingman: Not Started\n\n"
            "No input found. Add your requirements source to:\n"
            "  specs/00-inputs/user-description.md\n\n"
            "Then call swm_next again to begin Step 1."
        )

    if state == "STEP_1_READY":
        return "# Next: Step 1 (Discovery)\n\n" + swm_discover_context_tool(project_path)

    if state == "LOG_READY":
        return "# Next: Step 7 (Log)\n\n" + swm_log_context_tool(project_path)

    if state == "STEP_2_READY":
        return "# Next: Step 2 (Requirements)\n\n" + swm_extract_context_tool(project_path)

    if state == "STEP_3_PHASE1_READY":
        return "# Next: Step 3 Phase 1 (Clarify — Generate Questions)\n\n" + swm_clarify_context_tool(project_path)

    if state == "STEP_3_WAITING":
        open_q = root / "specs" / "01-discovery" / "open-questions.md"
        questions = open_q.read_text(encoding="utf-8") if open_q.exists() else "(no questions found)"
        return (
            "# SpecWingman: Waiting for Clarification\n\n"
            "Step 3 is paused. Show the questions below to the user and collect answers.\n\n"
            "Once answered, call:\n"
            "  swm_write_clarify(project_path, open_questions=<current content>, answer_draft=<user answers>)\n\n"
            "Then call swm_next again to run Phase 2 backfill.\n\n"
            "## Open Questions\n\n"
            + questions
        )

    if state == "STEP_3_PHASE2_READY":
        return "# Next: Step 3 Phase 2 (Clarify — Backfill)\n\n" + swm_clarify_context_tool(project_path)

    if state == "STEP_4_READY":
        return "# Next: Step 4 (Analyze)\n\n" + swm_analyze_context_tool(project_path)

    if state == "STEP_5_READY":
        return "# Next: Step 5 (Spec)\n\n" + swm_spec_context_tool(project_path)

    if state == "STEP_6_READY":
        return "# Next: Step 6 (Design)\n\n" + swm_design_context_tool(project_path)

    if state == "COMPLETE":
        return (
            "# SpecWingman: Workflow Complete\n\n"
            "All steps are done and the changelog is current.\n\n"
            "  specs/01-discovery/     — Discovery artifacts\n"
            "  specs/02-requirements/  — Formal requirements\n"
            "  specs/03-analysis/      — Analysis documents\n"
            "  specs/04-design-ready/  — Specification and design files\n"
            "  specs/05-versions/      — Changelog and decision log"
        )

    return f"Unknown state: {state}"
