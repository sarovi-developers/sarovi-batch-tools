import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from batch import parser, run

class Api:
    def __init__(self, failure=False): self.calls = []; self.failure = failure
    def chat(self, messages, key, **options):
        self.calls.append((messages, key, options))
        if self.failure: raise TimeoutError("uncertain request")
        return {"choices": [{"message": {"content": "سلام"}, "finish_reason": "stop"}], "usage": {"total_tokens": 12}}, "fixture-receipt"

class BatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.input = self.root / "input.csv"
        self.input.write_text('id,text\n1,Hello\n2,World\n', encoding="utf-8")
        self.output = self.root / "result.jsonl"
    def tearDown(self): self.tmp.cleanup()
    def args(self, *extra):
        return parser().parse_args(["translate", str(self.input), "--output", str(self.output), *extra])
    def test_default_is_zero_network_dry_run(self):
        api = Api()
        with contextlib.redirect_stdout(io.StringIO()): run(self.args(), api)
        self.assertFalse(self.output.exists()); self.assertEqual(api.calls, [])
    def test_resume_never_resends_completed_rows(self):
        api = Api()
        with contextlib.redirect_stdout(io.StringIO()):
            run(self.args("--run"), api); run(self.args("--run", "--resume"), api)
        self.assertEqual(len(api.calls), 2)
        self.assertNotEqual(api.calls[0][1], api.calls[1][1])
    def test_uncertain_send_blocks_resume(self):
        api = Api(failure=True)
        with self.assertRaisesRegex(RuntimeError, "No retry"): run(self.args("--run"), api)
        with self.assertRaisesRegex(ValueError, "Unresolved row"): run(self.args("--run", "--resume"), api)
        self.assertEqual(len(api.calls), 1)
    def test_changed_input_cannot_reuse_the_checkpoint(self):
        with contextlib.redirect_stdout(io.StringIO()): run(self.args("--demo"))
        self.input.write_text("text\nDifferent\n")
        with self.assertRaisesRegex(ValueError, "settings changed"): run(self.args("--demo", "--resume"))
    def test_demo_is_obviously_labeled_and_never_uses_api(self):
        api = Api(failure=True)
        with contextlib.redirect_stdout(io.StringIO()): run(self.args("--demo"), api)
        events = [json.loads(x) for x in self.output.read_text().splitlines()]
        self.assertTrue(events[0]["settings"]["demo"])
        self.assertTrue(events[2]["result"].startswith("[Offline demo]"))
        self.assertEqual(api.calls, [])
    def test_row_and_output_limits_are_enforced(self):
        for extra in [("--limit", "101"), ("--max-tokens", "99999")]:
            with self.assertRaises(ValueError): run(self.args(*extra))
        self.input.write_text("text\n" + "a" * 8001)
        with self.assertRaisesRegex(ValueError, "8,000"): run(self.args("--run"), Api())

if __name__ == "__main__": unittest.main()
