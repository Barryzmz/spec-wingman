import tempfile
import unittest
from pathlib import Path

from tools.analyze import swm_analyze_context_tool, swm_write_analyze_tool
from tools.clarify import swm_clarify_context_tool, swm_write_clarify_tool
from tools.design import swm_design_context_tool, swm_write_design_tool
from tools.discover import swm_discover_context_tool, swm_write_discovery_tool
from tools.extract import swm_extract_context_tool, swm_write_extract_tool
from tools.log import swm_log_context_tool, swm_write_log_tool
from tools.orchestrator import swm_next_tool
from tools.spec import swm_spec_context_tool, swm_write_spec_tool
from tools.status import swm_status_tool


class TestProjectPathValidation(unittest.TestCase):
    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)
        self.invalid_project = self.tmp / "does-not-exist"

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def _assert_invalid_path(self, func, *args, **kwargs):
        with self.assertRaisesRegex(ValueError, "Invalid project path"):
            func(str(self.invalid_project), *args, **kwargs)
        self.assertFalse(self.invalid_project.exists())

    def test_context_tools_reject_invalid_project_path(self):
        for func in [
            swm_discover_context_tool,
            swm_extract_context_tool,
            swm_clarify_context_tool,
            swm_analyze_context_tool,
            swm_spec_context_tool,
            swm_design_context_tool,
            swm_log_context_tool,
            swm_status_tool,
            swm_next_tool,
        ]:
            with self.subTest(func=func.__name__):
                self._assert_invalid_path(func)

    def test_write_tools_reject_invalid_project_path(self):
        cases = [
            (
                swm_write_discovery_tool,
                dict(
                    source_summary="x",
                    extracted_facts="x",
                    open_questions="x",
                    assumptions="x",
                    glossary="x",
                ),
            ),
            (
                swm_write_extract_tool,
                dict(
                    product_vision="x",
                    functional_requirements="x",
                    business_rules="x",
                    data_requirements="x",
                    workflow_requirements="x",
                    permission_requirements="x",
                    non_functional_requirements="x",
                    user_roles="x",
                ),
            ),
            (swm_write_clarify_tool, dict(open_questions="x")),
            (
                swm_write_analyze_tool,
                dict(
                    use_cases="x",
                    user_stories="x",
                    acceptance_criteria="x",
                    domain_model="x",
                    state_transitions="x",
                    edge_cases="x",
                ),
            ),
            (swm_write_spec_tool, dict(requirement_spec="x")),
            (
                swm_write_design_tool,
                dict(
                    system_design_brief="x",
                    api_draft="x",
                    database_draft="x",
                    frontend_pages="x",
                    test_cases="x",
                    development_tasks="x",
                ),
            ),
            (swm_write_log_tool, dict(changelog="x", decision_log="x")),
        ]

        for func, kwargs in cases:
            with self.subTest(func=func.__name__):
                self._assert_invalid_path(func, **kwargs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
