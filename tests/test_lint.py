"""Smoke + unit tests for mcp-schema-lint. Stdlib unittest, no deps."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcpschemalint.loader import load_tools, get_input_schema
from mcpschemalint.linter import lint_file
from mcpschemalint.rules import ERROR, WARN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOD = os.path.join(ROOT, "fixtures", "good_server.json")
BAD = os.path.join(ROOT, "fixtures", "bad_server.json")


class TestLoader(unittest.TestCase):
    def test_loads_tools_key(self):
        self.assertEqual(len(load_tools(GOOD)), 2)

    def test_loads_bare_list(self):
        self.assertEqual(len(load_tools(BAD)), 3)

    def test_input_schema_accessor(self):
        tools = load_tools(GOOD)
        self.assertIsNotNone(get_input_schema(tools[0]))


class TestGoodServer(unittest.TestCase):
    def test_no_findings(self):
        result = lint_file(GOOD)
        self.assertEqual(result.counts[ERROR], 0)
        self.assertEqual(result.counts[WARN], 0)
        self.assertTrue(result.passed())
        self.assertTrue(result.passed(strict=True))


class TestBadServer(unittest.TestCase):
    def setUp(self):
        self.result = lint_file(BAD)

    def test_has_errors_and_fails(self):
        self.assertGreater(self.result.counts[ERROR], 0)
        self.assertFalse(self.result.passed())

    def test_required_unknown_property_flagged(self):
        rules = {f.rule for f in self.result.findings}
        self.assertIn("required-unknown-property", rules)   # 'timeout' not in properties

    def test_missing_name_and_schema_flagged(self):
        rules = {f.rule for f in self.result.findings}
        self.assertIn("name-missing", rules)
        self.assertIn("input-schema-missing", rules)

    def test_vague_description_flagged(self):
        rules = {f.rule for f in self.result.findings}
        self.assertIn("description-vague", rules)           # "This tool"

    def test_additional_properties_flagged(self):
        rules = {f.rule for f in self.result.findings}
        self.assertIn("additional-properties-not-false", rules)

    def test_clean_tool_in_bad_file_has_no_findings(self):
        # the 'search' tool in bad_server is well-formed; it should not appear
        search_findings = [f for f in self.result.findings if f.tool == "search"]
        self.assertEqual(search_findings, [])

    def test_tools_with_errors_count(self):
        # 'run' (bad required) and the nameless tool both have errors
        self.assertEqual(self.result.tools_with_errors, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
