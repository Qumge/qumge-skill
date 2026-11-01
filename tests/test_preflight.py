import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/qumge-publish/scripts/preflight.py"


def document():
    return {"qumge": "2", "connections": {"reporter": {"type": "api", "base_url": "https://api.vendor.org", "auth": "api_key"}},
            "capabilities": [{"slug": "row-summary", "name": "Row summary", "summary": "Numbers in, count and sum out.",
              "icon_url": "https://api.vendor.org/icon.png", "connection": "reporter", "operations": [{
              "name": "summarize_rows", "method": "POST", "path": "/summary", "description": "Summarize numbers.",
              "price_usd": 0.01, "input_schema": {"type": "object"}, "output_schema": {"type": "object"},
              "example_input": {"values": [2, 3, 5]}, "example_output": {"count": 3, "sum": 10},
              "execution": {"mode": "sync", "protocol": "native", "identity": "order", "idempotency": {"mode": "none"}}}]}]}


class PreflightTest(unittest.TestCase):
    def run_check(self, doc, *args, raw=None):
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "qumge.json"
            manifest.write_text(raw if raw is not None else json.dumps(doc))
            before = manifest.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(manifest), *args], capture_output=True, text=True)
            self.assertEqual(before, manifest.read_bytes())
            self.assertTrue(result.stdout, result.stderr)
            return result.returncode, json.loads(result.stdout)

    def test_local_checks_do_not_claim_deployment_or_delivery(self):
        code, report = self.run_check(document())
        self.assertEqual(0, code)
        self.assertEqual("passed", report["local_preflight"])
        self.assertIn("real_delivery", report["not_checked"])
        self.assertIn("deployment", report["not_checked"])
        self.assertIn("platform_validation", report["not_checked"])
        self.assertEqual("row-summary", report["slug"])
        self.assertEqual(64, len(report["manifest_file_sha256"]))

    def test_changed_manifest_changes_fingerprint(self):
        _, a = self.run_check(document())
        doc = document(); doc["capabilities"][0]["summary"] = "Changed result"
        _, b = self.run_check(doc)
        self.assertNotEqual(a["manifest_file_sha256"], b["manifest_file_sha256"])

    def test_secret_is_blocked_without_echoing_value(self):
        doc = document(); doc["connections"]["reporter"]["api_key"] = "sk_qumge_DO_NOT_PRINT"
        code, report = self.run_check(doc)
        self.assertEqual(1, code)
        self.assertNotIn("DO_NOT_PRINT", json.dumps(report))
        self.assertIn("secret_field", [x["code"] for x in report["findings"]])

    def test_missing_output_and_boolean_price_are_blocked(self):
        doc = document(); op = doc["capabilities"][0]["operations"][0]
        op.pop("output_schema"); op["price_usd"] = True
        code, report = self.run_check(doc)
        self.assertEqual(1, code)
        self.assertTrue(any(x["code"] == "output_schema" for x in report["findings"]))
        self.assertTrue(any(x["code"] == "price" for x in report["findings"]))

    def test_async_status_stays_private(self):
        doc = document(); ops = doc["capabilities"][0]["operations"]
        ops[0]["execution"].update(mode="async", status={"method": "GET", "path": "/jobs/{job_id}"})
        ops.append({"name": "job_status", "method": "GET", "path": "/jobs/{job_id}"})
        code, report = self.run_check(doc)
        self.assertEqual(1, code)
        self.assertIn("public_status", [x["code"] for x in report["findings"]])

    def test_async_without_status_is_blocked(self):
        doc = document(); doc["capabilities"][0]["operations"][0]["execution"]["mode"] = "async"
        self.assertEqual(1, self.run_check(doc)[0])

    def test_multiple_caps_require_explicit_selection(self):
        doc = document(); other = copy.deepcopy(doc["capabilities"][0]); other["slug"] = "other"; doc["capabilities"].append(other)
        self.assertEqual(1, self.run_check(doc)[0])
        code, report = self.run_check(doc, "--slug", "other")
        self.assertEqual(0, code)
        self.assertEqual("other", report["slug"])

    def test_malformed_duplicate_and_nonfinite_json_are_diagnostics(self):
        for raw in ['{', '{"qumge":"2","qumge":"1"}', '{"qumge":NaN}']:
            with self.subTest(raw=raw):
                code, report = self.run_check(None, raw=raw)
                self.assertEqual(1, code)
                self.assertEqual("json", report["findings"][0]["code"])

    def test_placeholder_or_local_url_is_not_publish_ready(self):
        for url in ["http://localhost:3000", "https://api.example.com", "https://user:pass@api.vendor.org", "https://api.vendor.org?token=hidden"]:
            doc = document(); doc["connections"]["reporter"]["base_url"] = url
            self.assertEqual(1, self.run_check(doc)[0])

    def test_report_destination_cannot_overwrite_manifest_or_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "qumge.json"; manifest.write_text(json.dumps(document()))
            existing = Path(folder) / "notes.json"; existing.write_text("keep me")
            for target in [manifest, existing]:
                result = subprocess.run([sys.executable, str(SCRIPT), str(manifest), "--report", str(target)], capture_output=True, text=True)
                self.assertEqual(2, result.returncode)
            self.assertEqual("keep me", existing.read_text())
            self.assertEqual(document(), json.loads(manifest.read_text()))
            report = Path(folder) / "reports" / "preflight.json"
            result = subprocess.run([sys.executable, str(SCRIPT), str(manifest), "--report", str(report)], capture_output=True, text=True)
            self.assertEqual(0, result.returncode)
            self.assertEqual(json.loads(result.stdout), json.loads(report.read_text()))

    def test_wrong_json_shapes_produce_findings_not_tracebacks(self):
        variants = []
        doc = document(); doc["capabilities"][0]["connection"] = []; variants.append(doc)
        doc = document(); doc["connections"]["reporter"] = []; variants.append(doc)
        for key in ("type", "auth"):
            doc = document(); doc["connections"]["reporter"][key] = []; variants.append(doc)
        for key in ("mode", "protocol", "identity"):
            doc = document(); doc["capabilities"][0]["operations"][0]["execution"][key] = []; variants.append(doc)
        doc = document(); doc["capabilities"][0]["operations"][0]["execution"]["idempotency"]["mode"] = []; variants.append(doc)
        for doc in variants:
            with self.subTest(doc=doc):
                self.assertEqual(1, self.run_check(doc)[0])

    def test_extreme_numeric_price_is_a_diagnostic(self):
        doc = document(); doc["capabilities"][0]["operations"][0]["price_usd"] = 10 ** 400
        self.assertEqual(1, self.run_check(doc)[0])

    def test_checker_never_opens_network(self):
        spec = importlib.util.spec_from_file_location("preflight", SCRIPT)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with patch("socket.create_connection", side_effect=AssertionError("network forbidden")), patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")):
            self.assertEqual("passed", module.inspect_manifest(document())["local_preflight"])


if __name__ == "__main__":
    unittest.main()
