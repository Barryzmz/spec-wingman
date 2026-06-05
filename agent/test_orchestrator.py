"""
Unit tests for the orchestrator state machine (determine_state).

Each test creates a minimal temp directory that mimics a specific point
in the SpecWingman workflow and asserts the expected state string.
Timestamps are manipulated via os.utime so the log-is-current check
behaves deterministically without relying on wall-clock ordering.
"""

import os
import time
import tempfile
import unittest
from pathlib import Path

from tools.orchestrator import determine_state

# Timestamps: "old" = 100 s ago, "new" = now
_OLD = time.time() - 100
_NEW = time.time()


def _touch(path: Path, content: str = "content", mtime: float = _NEW) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    os.utime(path, (_NEW, mtime))
    return path


def _make_base(tmp: Path) -> None:
    """Scaffold the project skeleton (no specs files yet)."""
    (tmp / "CONSTITUTION.md").write_text("constitution", encoding="utf-8")
    for p in ["prompts", "templates", "specs/00-inputs",
              "specs/01-discovery", "specs/02-requirements",
              "specs/03-analysis", "specs/04-design-ready",
              "specs/05-versions"]:
        (tmp / p).mkdir(parents=True, exist_ok=True)


_STEP1_FILES = ["source-summary.md", "extracted-facts.md",
                "open-questions.md", "assumptions.md", "glossary.md"]
_STEP2_FILES = ["product-vision.md", "functional-requirements.md", "business-rules.md",
                "data-requirements.md", "workflow-requirements.md",
                "permission-requirements.md", "non-functional-requirements.md",
                "user-roles.md"]
_STEP4_FILES = ["use-cases.md", "user-stories.md", "acceptance-criteria.md",
                "domain-model.md", "state-transitions.md", "edge-cases.md"]
_STEP6_FILES = ["system-design-brief.md", "api-draft.md", "database-draft.md",
                "frontend-pages.md", "test-cases.md", "development-tasks.md"]


def _write_step(tmp: Path, subdir: str, files: list[str], mtime: float = _NEW) -> None:
    for f in files:
        _touch(tmp / "specs" / subdir / f, mtime=mtime)


def _write_log(tmp: Path, mtime: float = _NEW, steps: tuple[int, ...] = (1, 2, 3, 4, 5, 6)) -> None:
    changelog = "\n".join(
        f"| 0.{step}.0 / 2026-06-06 00:00:00 +08:00 | specs | Logged step {step} | completed | Step {step} - swm.step |"
        for step in steps
    )
    _touch(tmp / "specs" / "05-versions" / "changelog.md", content=changelog, mtime=mtime)
    _touch(tmp / "specs" / "05-versions" / "decision-log.md", content="No decisions", mtime=mtime)


class TestDetermineState(unittest.TestCase):

    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)
        _make_base(self.tmp)

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def p(self) -> str:
        return str(self.tmp)

    # ── NOT_STARTED ────────────────────────────────────────────────────────────

    def test_not_started_no_file(self):
        self.assertEqual(determine_state(self.p()), "NOT_STARTED")

    def test_not_started_empty_file(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", content="   ")
        self.assertEqual(determine_state(self.p()), "NOT_STARTED")

    # ── STEP_1_READY ───────────────────────────────────────────────────────────

    def test_step1_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md")
        self.assertEqual(determine_state(self.p()), "STEP_1_READY")

    def test_step1_ready_partial_discovery(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md")
        _touch(self.tmp / "specs" / "01-discovery" / "source-summary.md")
        self.assertEqual(determine_state(self.p()), "STEP_1_READY")

    # ── LOG_READY after step 1 ─────────────────────────────────────────────────

    def test_log_ready_after_step1(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_NEW)
        # No changelog → log not current
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step1_stale_changelog(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)  # changelog older than discovery files
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    # ── STEP_2_READY ───────────────────────────────────────────────────────────

    def test_step2_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)  # log is current
        self.assertEqual(determine_state(self.p()), "STEP_2_READY")

    # ── LOG_READY after step 2 ─────────────────────────────────────────────────

    def test_log_ready_after_step2(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)  # stale
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    # ── STEP_3_PHASE1_READY ───────────────────────────────────────────────────

    def test_step3_phase1_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_3_PHASE1_READY")

    # ── LOG_READY between phase 1 and WAITING ─────────────────────────────────

    def test_log_ready_after_step3_phase1(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        # Requirements written at _OLD
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        # Phase 1: open-questions rewritten at _NEW (newer than requirements)
        _touch(self.tmp / "specs" / "01-discovery" / "open-questions.md", mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)  # log stale
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    # ── STEP_3_WAITING ────────────────────────────────────────────────────────

    def test_step3_waiting(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        # Phase 1: open-questions newer than requirements
        _touch(self.tmp / "specs" / "01-discovery" / "open-questions.md", mtime=_NEW)
        _write_log(self.tmp, mtime=_NEW)  # log current
        self.assertEqual(determine_state(self.p()), "STEP_3_WAITING")

    # ── STEP_3_PHASE2_READY ───────────────────────────────────────────────────

    def test_step3_phase2_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md",
               content="User answers here", mtime=_NEW)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_3_PHASE2_READY")

    # ── STEP_4_READY (step 3 DONE) ────────────────────────────────────────────

    def test_step4_ready_after_step3_done(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        # Step 3 DONE: answer-draft exists but is empty
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md",
               content="", mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_4_READY")

    # ── LOG_READY after step 4 ────────────────────────────────────────────────

    def test_log_ready_after_step4(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md", content="", mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    def test_log_ready_after_step4_when_changelog_missing_step4(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "01-discovery" / "answer-draft.md", content="", mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW, steps=(1, 2, 3))
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    # ── STEP_5_READY ──────────────────────────────────────────────────────────

    def test_step5_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_5_READY")

    # ── LOG_READY after step 5 ────────────────────────────────────────────────

    def test_log_ready_after_step5(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "04-design-ready" / "requirement-spec.md", mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

    # ── STEP_6_READY ──────────────────────────────────────────────────────────

    def test_step6_ready(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "04-design-ready" / "requirement-spec.md", mtime=_OLD)
        _write_log(self.tmp, mtime=_NEW)
        self.assertEqual(determine_state(self.p()), "STEP_6_READY")

    # ── LOG_READY after step 6 ────────────────────────────────────────────────

    def test_log_ready_after_step6(self):
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md", mtime=_OLD)
        _write_step(self.tmp, "01-discovery", _STEP1_FILES, mtime=_OLD)
        _write_step(self.tmp, "02-requirements", _STEP2_FILES, mtime=_OLD)
        _write_step(self.tmp, "03-analysis", _STEP4_FILES, mtime=_OLD)
        _touch(self.tmp / "specs" / "04-design-ready" / "requirement-spec.md", mtime=_OLD)
        _write_step(self.tmp, "04-design-ready", _STEP6_FILES, mtime=_NEW)
        _write_log(self.tmp, mtime=_OLD)
        self.assertEqual(determine_state(self.p()), "LOG_READY")

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

    # ── swm_next smoke test ───────────────────────────────────────────────────

    def test_swm_next_routes_correctly(self):
        from tools.orchestrator import swm_next_tool
        # NOT_STARTED should not crash and return a message
        result = swm_next_tool(self.p())
        self.assertIn("Not Started", result)

        # STEP_1_READY
        _touch(self.tmp / "specs" / "00-inputs" / "user-description.md")
        result = swm_next_tool(self.p())
        self.assertIn("Step 1", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
