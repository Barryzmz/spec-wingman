import tempfile
import unittest
from pathlib import Path

from tools.status import _has_substantive_content


class TestStatusContentDetection(unittest.TestCase):
    def setUp(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)

    def tearDown(self):
        self._tmp_ctx.cleanup()

    def _file(self, content: str) -> Path:
        path = self.tmp / "artifact.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_template_table_rows_are_not_substantive(self):
        path = self._file(
            """# Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | TBD | Pending |
"""
        )
        self.assertFalse(_has_substantive_content(path))

    def test_real_table_data_row_is_substantive(self):
        path = self._file(
            """# Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | User can export a spec bundle. | Confirmed |
"""
        )
        self.assertTrue(_has_substantive_content(path))

    def test_blockquote_guidance_is_not_substantive(self):
        path = self._file(
            """# Notes

> Fill in this section after discovery.
"""
        )
        self.assertFalse(_has_substantive_content(path))

    def test_label_placeholder_is_not_substantive(self):
        path = self._file("Requirement: TBD\n")
        self.assertFalse(_has_substantive_content(path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
