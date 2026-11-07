"""Preproduction regression tests for the authored curriculum."""

import importlib.util
from pathlib import Path


def test_all_reference_solutions_and_map_metadata():
    script = Path(__file__).resolve().parents[1] / "tools/check_content.py"
    spec = importlib.util.spec_from_file_location("check_content", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.check_all()
