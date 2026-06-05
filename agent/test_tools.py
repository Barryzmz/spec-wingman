"""
SpecWingman agent tools test suite.

Covers:
  - BUG-001 ~ BUG-005 regression tests
  - Orchestrator state machine (determine_state) full coverage

Run:  .venv\\Scripts\\python.exe -m unittest test_tools -v
"""

import os
import re
import tempfile
import time
import unittest
from pathlib import Path

from tools.analyze import swm_analyze_context_tool, swm_write_analyze_tool
from tools.clarify import swm_clarify_context_tool, swm_write_clarify_tool
from tools.design import swm_design_context_tool, swm_write_design_tool
from tools.discover import swm_discover_context_tool, swm_write_discovery_tool
from tools.extract import swm_extract_context_tool, swm_write_extract_tool
from tools.log import swm_log_context_tool, swm_write_log_tool
from tools.orchestrator import determine_state, swm_next_tool
from tools.spec import swm_spec_context_tool, swm_write_spec_tool
from tools.status import swm_status_tool, _has_substantive_content

_OLD = time.time() - 100
_NEW = time.time()

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ── Shared helpers ────────────────────────────────────────────────────────────

def _touch(path: Path, content: str = "content", mtime: float = _NEW) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    os.utime(path, (_NEW, mtime))
    return path


def _make_base(tmp: Path) -> None:
    (tmp / "CONSTITUTION.md").write_text("constitution", encoding="utf-8")
    for p in [
        "prompts", "templates", "specs/00-inputs",
        "specs/01-discovery", "specs/02-requirements",
        "specs/03-analysis", "specs/04-design-ready",
        "specs/05-versions",
    ]:
        (tmp / p).mkdir(parents=True, exist_ok=True)


_STEP1_FILES = [
    "source-summary.md", "extracted-facts.md",
    "open-questions.md", "assumptions.md", "glossary.md",
]
_STEP2_FILES = [
    "product-vision.md", "functional-requirements.md", "business-rules.md",
    "data-requirements.md", "workflow-requirements.md",
    "permission-requirements.md", "non-functional-requirements.md",
    "user-roles.md",
]
_STEP4_FILES = [
    "use-cases.md", "user-stories.md", "acceptance-criteria.md",
    "domain-model.md", "state-transitions.md", "edge-cases.md",
]
_STEP6_FILES = [
    "system-design-brief.md", "api-draft.md", "database-draft.md",
    "frontend-pages.md", "test-cases.md", "development-tasks.md",
]


def _write_step(tmp: Path, subdir: str, files: list[str], mtime: float = _NEW) -> None:
    for f in files:
        _touch(tmp / "specs" / subdir / f, mtime=mtime)


def _write_log(tmp: Path, mtime: float = _NEW, steps: tuple[int, ...] = (1, 2, 3, 4, 5, 6)) -> None:
    changelog = "\n".join(
        f"| 0.{s}.0 / 2026-06-06 00:00:00 +08:00 | specs | Logged step {s} | completed | Step {s} - swm.step |"
        for s in steps
    )
    _touch(tmp / "specs" / "05-versions" / "changelog.md", content=changelog, mtime=mtime)
    _touch(tmp / "specs" / "05-versions" / "decision-log.md", content="No decisions", mtime=mtime)


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-001: swm_write_* tools 對錯誤 project_path 無防護
# ═══════════════════════════════════════════════════════════════════════════════
class TestBug001_WriteToolsRejectInvalidPath(unittest.TestCase):
    """All 7 write tools must raise ValueError for non-existent project path."""

    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.bad_path = str(Path(self._tmp_ctx.name) / "does-not-exist")

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def _assert_rejects(self, func, **kwargs):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            func(self.bad_path, **kwargs)
        self.assertFalse(Path(self.bad_path).exists(),
                         "Must NOT create orphan directories on invalid path")

    def test_write_discovery(self):
        self._assert_rejects(swm_write_discovery_tool,
                             source_summary="x", extracted_facts="x",
                             open_questions="x", assumptions="x", glossary="x")

    def test_write_extract(self):
        self._assert_rejects(swm_write_extract_tool,
                             product_vision="x", functional_requirements="x",
                             business_rules="x", data_requirements="x",
                             workflow_requirements="x", permission_requirements="x",
                             non_functional_requirements="x", user_roles="x")

    def test_write_clarify(self):
        self._assert_rejects(swm_write_clarify_tool, open_questions="x")

    def test_write_analyze(self):
        self._assert_rejects(swm_write_analyze_tool,
                             use_cases="x", user_stories="x",
                             acceptance_criteria="x", domain_model="x",
                             state_transitions="x", edge_cases="x")

    def test_write_spec(self):
        self._assert_rejects(swm_write_spec_tool, requirement_spec="x")

    def test_write_design(self):
        self._assert_rejects(swm_write_design_tool,
                             system_design_brief="x", api_draft="x",
                             database_draft="x", frontend_pages="x",
                             test_cases="x", development_tasks="x")

    def test_write_log(self):
        self._assert_rejects(swm_write_log_tool, changelog="x", decision_log="x")


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-002: swm_*_context tools 對錯誤 project_path 靜默回傳空內容
# ═══════════════════════════════════════════════════════════════════════════════
class TestBug002_ContextToolsRejectInvalidPath(unittest.TestCase):
    """All 7 context tools + status + next must raise ValueError."""

    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.bad_path = str(Path(self._tmp_ctx.name) / "does-not-exist")

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def test_discover_context(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_discover_context_tool(self.bad_path)

    def test_extract_context(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_extract_context_tool(self.bad_path)

    def test_clarify_context(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_clarify_context_tool(self.bad_path)

    def test_analyze_context(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_analyze_context_tool(self.bad_path)

    def test_spec_context(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_spec_context_tool(self.bad_path)

    def test_design_context(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_design_context_tool(self.bad_path)

    def test_log_context(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_log_context_tool(self.bad_path)

    def test_status(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_status_tool(self.bad_path)

    def test_next(self):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            swm_next_tool(self.bad_path)

    def test_directory_exists_but_no_constitution(self):
        """A real directory without CONSTITUTION.md should also be rejected."""
        real_dir = Path(self._tmp_ctx.name)
        with self.assertRaisesRegex(ValueError, "CONSTITUTION.md not found"):
            swm_status_tool(str(real_dir))


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-003: swm_status 只檢查檔案存在不檢查內容
# ═══════════════════════════════════════════════════════════════════════════════
class TestBug003_StatusContentDetection(unittest.TestCase):
    """_has_substantive_content must distinguish TBD templates from real data."""

    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def _file(self, content: str) -> Path:
        path = self.tmp / "artifact.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_tbd_table_rows_not_substantive(self):
        path = self._file(
            "| ID | Requirement | Status |\n"
            "|----|-------------|--------|\n"
            "| FR-001 | TBD | Pending |\n"
        )
        self.assertFalse(_has_substantive_content(path))

    def test_real_table_data_is_substantive(self):
        path = self._file(
            "| ID | Requirement | Status |\n"
            "|----|-------------|--------|\n"
            "| FR-001 | User can export a spec bundle. | Confirmed |\n"
        )
        self.assertTrue(_has_substantive_content(path))

    def test_blockquote_guidance_not_substantive(self):
        path = self._file("> Fill in this section after discovery.\n")
        self.assertFalse(_has_substantive_content(path))

    def test_plain_tbd_label_not_substantive(self):
        path = self._file("Requirement: TBD\n")
        self.assertFalse(_has_substantive_content(path))

    def test_empty_file_not_substantive(self):
        path = self._file("")
        self.assertFalse(_has_substantive_content(path))

    def test_headers_only_not_substantive(self):
        path = self._file("# Section Title\n\n## Sub Section\n")
        self.assertFalse(_has_substantive_content(path))

    def test_real_prose_is_substantive(self):
        path = self._file(
            "# Notes\n\nThe user requires OAuth2 integration with Google.\n"
        )
        self.assertTrue(_has_substantive_content(path))

    def test_status_tool_shows_three_states(self):
        """swm_status on a real project must distinguish ok / template / empty."""
        tmp = self.tmp / "proj"
        tmp.mkdir()
        _make_base(tmp)
        _touch(tmp / "specs" / "00-inputs" / "user-description.md", content="real input")
        _touch(tmp / "specs" / "01-discovery" / "source-summary.md", content="real data")
        _touch(tmp / "specs" / "01-discovery" / "extracted-facts.md", content="TBD")
        result = swm_status_tool(str(tmp))
        self.assertIn("[ok]", result, "Files with real content should show [ok]")
        self.assertIn("[template]", result, "TBD-only files should show [template]")
        self.assertIn("[empty]", result, "Steps with no files should show [empty]")


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-004: /swm.log 無變更時缺少防呆
# ═══════════════════════════════════════════════════════════════════════════════
class TestBug004_LogPromptGuardClause(unittest.TestCase):
    """The 07-update-versions prompt must contain a guard clause against duplicates."""

    def test_prompt_has_guard_clause(self):
        prompt_path = _PROJECT_ROOT / "prompts" / "07-update-versions.prompt.md"
        self.assertTrue(prompt_path.exists(), f"Prompt file not found: {prompt_path}")
        content = prompt_path.read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r"guard\s+clause", content, re.IGNORECASE),
            "Prompt must contain 'guard clause' instruction to prevent duplicate entries"
        )
        self.assertIn("Related Prompt Step", content,
                      "Prompt must require 'Related Prompt Step' field")

    def test_prompt_prevents_rewriting_history(self):
        prompt_path = _PROJECT_ROOT / "prompts" / "07-update-versions.prompt.md"
        content = prompt_path.read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r"(missing|stale|materially changed)", content),
            "Prompt must specify to only update missing/stale/changed entries"
        )
        self.assertTrue(
            re.search(r"not rewrite.*(unrelated|historical)", content, re.IGNORECASE),
            "Prompt must instruct not to rewrite unrelated historical entries"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# BUG-005: swm_next 缺少 LOG_READY 檢查
# ═══════════════════════════════════════════════════════════════════════════════
class TestBug005_NextLogReadyGuard(unittest.TestCase):
    """swm_next must return LOG_READY before advancing when changelog is stale."""

    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)
        _make_base(self.tmp)

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def p(self) -> str:
        return str(self.tmp)

    def test_log_ready_after_step1_no_changelog(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step1_stale_changelog(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step2(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step4(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md", content="", mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step4_changelog_missing_step(self):
        """Changelog records steps 1-3 but step 4 is complete -> LOG_READY."""
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md", content="", mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW, steps=(1, 2, 3))
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step5(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "04-design-ready" / "requirement-spec.md", mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step6(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "04-design-ready" / "requirement-spec.md", mtime=_OLD)
        _write_step(self.tmp, "04-design-ready", _STEP6_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_swm_next_returns_log_message(self):
        """swm_next_tool must include 'Log' in response when LOG_READY."""
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_NEW)
        result = swm_next_tool(self.p())
        self.assertIn("Log", result)

    def test_advances_only_when_log_current(self):
        """After log is updated, state should advance to next step."""
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_2_READY")


# ═══════════════════════════════════════════════════════════════════════════════
# Orchestrator state machine — full workflow progression
# ═══════════════════════════════════════════════════════════════════════════════
class TestOrchestratorStateMachine(unittest.TestCase):
    """Verify determine_state returns the correct state at every workflow stage."""

    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)
        _make_base(self.tmp)

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def p(self) -> str:
        return str(self.tmp)

    # ── NOT_STARTED ───────────────────────────────────────────────────────────

    def test_not_started_no_file(self):
        self.assertEqual(determine_state(self.p()), "NOT_STARTED")

    def test_not_started_empty_file(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", content="   ")
        self.assertEqual(determine_state(self.p()), "NOT_STARTED")

    # ── STEP_1_READY ──────────────────────────────────────────────────────────

    def test_step1_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md")
        self.assertEqual(determine_state(self.p()), "STEP_1_READY")

    def test_step1_ready_partial_discovery(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md")
        _touch(self.tmp / "specs" / "01-discovery" / "source-summary.md")
        self.assertEqual(determine_state(self.p()), "STEP_1_READY")

    # ── STEP_2_READY ──────────────────────────────────────────────────────────

    def test_step2_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_2_READY")

    # ── STEP_3 phases ─────────────────────────────────────────────────────────

    def test_step3_phase1_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_3_PHASE1_READY")

    def test_step3_waiting(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "open-questions.md", mtime=_NEW)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_3_WAITING")

    def test_step3_phase2_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md",
               content="User answers here", mtime=_NEW)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_3_PHASE2_READY")

    def test_step3_log_ready_after_phase1(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "open-questions.md", mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    # ── STEP_4_READY ──────────────────────────────────────────────────────────

    def test_step4_ready_after_step3_done(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md",
               content="", mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_4_READY")

    # ── STEP_5_READY ──────────────────────────────────────────────────────────

    def test_step5_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_5_READY")

    # ── STEP_6_READY ──────────────────────────────────────────────────────────

    def test_step6_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "04-design-ready" / "requirement-spec.md", mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_6_READY")

    # ── COMPLETE ──────────────────────────────────────────────────────────────

    def test_complete(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "04-design-ready" / "requirement-spec.md", mtime=_OLD)
        _write_step(self.tmp, "04-design-ready", _STEP6_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "COMPLETE")

    # ── swm_next routing smoke test ───────────────────────────────────────────

    def test_swm_next_not_started(self):
        result = swm_next_tool(self.p())
        self.assertIn("Not Started", result)

    def test_swm_next_step1(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md")
        result = swm_next_tool(self.p())
        self.assertIn("Step 1", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
