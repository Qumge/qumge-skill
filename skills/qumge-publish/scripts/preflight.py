#!/usr/bin/env python3
"""Offline managed-v2 readiness checks, not a full JSON Schema or platform validator."""
import argparse
import hashlib
import ipaddress
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

NOT_CHECKED = ["full_json_schema", "deployment", "provider_authentication", "platform_validation", "owner_authorization", "real_delivery"]
SECRET_KEY = re.compile(r"token|secret|password|api_key", re.I)


def inspect_manifest(document, slug=None):
    findings = []
    def issue(code, path, action):
        findings.append({"code": code, "path": path, "action": action})

    def secret_scan(value, path=""):
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(item, str) and SECRET_KEY.search(key):
                    issue("secret_field", path, "Remove credential fields from the public manifest; configure private connection credentials separately.")
                else:
                    secret_scan(item, path + "/" + key.replace("~", "~0").replace("/", "~1"))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                secret_scan(item, path + "/" + str(i))

    def https_url(value, path):
        try:
            url = urlsplit(value if isinstance(value, str) else "")
            host = url.hostname or ""
            _ = url.port
            invalid = url.scheme != "https" or not host or bool(url.username or url.password or url.query or url.fragment)
            invalid = invalid or bool(re.search(r"[\s\\]", value or "")) or unquote(url.path).split("/").count("..") > 0
            invalid = invalid or host in {"localhost", "example.com", "example.org", "example.net"} or host.endswith((".localhost", ".local", ".example.com", ".example.org", ".example.net"))
            try:
                invalid = invalid or not ipaddress.ip_address(host).is_global
            except ValueError:
                pass
            if invalid:
                raise ValueError()
        except (ValueError, TypeError):
            issue("https_url", path, "Set a real HTTPS URL without credentials, query, fragment, local host or example-domain placeholder; reachability is checked after deployment.")

    selected = None
    if not isinstance(document, dict):
        issue("document", "", "Use a JSON object with qumge, connections and capabilities.")
    else:
        secret_scan(document)
        if document.get("qumge") != "2":
            issue("version", "/qumge", "Use the current managed manifest version string 2; keep legacy integrations on their existing maintenance path.")
        connections = document.get("connections")
        caps = document.get("capabilities")
        if not isinstance(connections, dict) or not connections:
            issue("connections", "/connections", "Declare named provider connections.")
            connections = {}
        for name, endpoint in connections.items():
            path = "/connections/" + name
            if not isinstance(endpoint, dict) or endpoint.get("type") not in ("api", "mcp") or endpoint.get("auth") not in ("signed", "api_key"):
                issue("connection", path, "Declare an api or mcp connection and supported provider authentication.")
                continue
            https_url(endpoint.get("mcp_url" if endpoint["type"] == "mcp" else "base_url"), path)
            if endpoint["type"] == "mcp" and endpoint["auth"] == "signed":
                issue("connection", path, "Native MCP connections use provider API-key authentication.")
        if not isinstance(caps, list) or not caps or not all(isinstance(c, dict) for c in caps):
            issue("capabilities", "/capabilities", "Declare at least one capability object.")
            caps = []
        matches = [c for c in caps if c.get("slug") == slug] if slug else caps
        if len(matches) != 1:
            issue("selection", "/capabilities", "Use --slug to select exactly one capability; slugs must be unique.")
        else:
            selected = matches[0]
        for i, cap in enumerate(caps):
            path = "/capabilities/" + str(i)
            for field in ("name", "summary", "slug", "connection"):
                if not isinstance(cap.get(field), str) or not cap[field].strip():
                    issue("capability", path + "/" + field, "Supply a non-empty public identity and named connection.")
            if isinstance(cap.get("slug"), str) and not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,59}", cap["slug"]):
                issue("slug", path + "/slug", "Use a stable lowercase slug of at most 60 characters.")
            if not isinstance(cap.get("connection"), str) or cap["connection"] not in connections:
                issue("connection", path + "/connection", "Reference a declared connection.")
            https_url(cap.get("icon_url"), path + "/icon_url")
            operations = cap.get("operations")
            if not isinstance(operations, list) or not operations or not all(isinstance(o, dict) for o in operations):
                issue("operations", path + "/operations", "Declare complete-result operations.")
                continue
            priced = [o for o in operations if "price_usd" in o]
            if not priced:
                issue("price", path, "Declare a fixed price for the complete result; a suggested price is not owner approval.")
            endpoint = connections.get(cap.get("connection"), {}) if isinstance(cap.get("connection"), str) else {}
            if not isinstance(endpoint, dict):
                endpoint = {}
            for j, operation in enumerate(priced):
                at = path + "/priced_operations/" + str(j)
                price = operation.get("price_usd")
                if type(price) not in (int, float) or not 0.001 <= price <= 50 or not math.isfinite(price):
                    issue("price", at, "Use a finite USD number within the current published manifest range; confirm initial pricing with the owner.")
                if not operation.get("description"):
                    issue("description", at, "Describe the complete buyer deliverable.")
                if endpoint.get("type") == "api":
                    if operation.get("method") not in ("GET", "POST", "PUT", "PATCH", "DELETE") or not isinstance(operation.get("path"), str) or not re.fullmatch(r"/[^*{}\s?#]*", operation["path"]):
                        issue("route", at, "Declare an exact HTTP method and path.")
                elif not operation.get("tool"):
                    issue("route", at, "Declare the native MCP tool name.")
                for field in ("input_schema", "output_schema"):
                    if not isinstance(operation.get(field), dict) or not operation[field]:
                        issue(field, at, "Provide the complete JSON schema; this checker does not validate schemas or examples against it.")
                for field in ("example_input", "example_output"):
                    if field not in operation or operation[field] is None:
                        issue(field, at, "Supply a non-null representative example, not a claim of real delivery.")
                execution = operation.get("execution")
                if not isinstance(execution, dict):
                    issue("execution", at, "Declare managed execution mode, protocol, identity and truthful idempotency.")
                    continue
                if execution.get("mode") not in ("sync", "async") or execution.get("protocol") not in ("native", "qumge") or execution.get("identity") not in ("order", "buyer"):
                    issue("execution", at, "Choose supported execution mode/protocol and order identity unless buyer-owned access is explicitly authorized.")
                idem = execution.get("idempotency", {})
                if not isinstance(idem, dict) or idem.get("mode") not in ("none", "native", "lookup"):
                    issue("idempotency", at, "Declare implemented durable deduplication or truthfully use none; do not invent native support.")
                elif idem.get("mode") == "lookup" and not idem.get("lookup"):
                    issue("idempotency", at, "Provide the private lookup mapping.")
                status = execution.get("status")
                if execution.get("mode") == "async" and (not isinstance(status, dict) or not (status.get("path") or status.get("tool"))):
                    issue("async_status", at, "Map the private native job status operation before platform testing.")
                if isinstance(status, dict):
                    for other in operations:
                        same = status.get("tool") and status.get("tool") == other.get("tool")
                        same = same or (status.get("path") and status.get("path") == other.get("path") and status.get("method") == other.get("method"))
                        if same:
                            issue("public_status", at, "Keep provider status private; buyers read the free platform job ID through get_cap_job.")
    return {"report_version": 1, "scope": "offline_local_readiness", "local_preflight": "blocked" if findings else "passed",
            "slug": selected.get("slug") if selected and isinstance(selected.get("slug"), str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,59}", selected["slug"]) else None, "findings": findings, "not_checked": NOT_CHECKED.copy(),
            "next_action": "fix_local_findings" if findings else "review_authorization_and_deployment_then_create_or_reconcile_draft"}


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--slug")
    parser.add_argument("--report", type=Path, help="Create a new report file; existing files are never overwritten.")
    args = parser.parse_args()
    digest = None
    try:
        raw = args.manifest.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        document = json.loads(raw, object_pairs_hook=strict_object, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite")))
        report = inspect_manifest(document, args.slug)
    except (OSError, ValueError, UnicodeError, RecursionError):
        report = {"report_version": 1, "scope": "offline_local_readiness", "local_preflight": "blocked", "slug": None,
                  "findings": [{"code": "json", "path": "", "action": "Read a valid UTF-8 JSON file without duplicate keys or non-finite values; raw input is not echoed."}],
                  "not_checked": NOT_CHECKED.copy(), "next_action": "fix_local_findings"}
    report["manifest_file_sha256"] = digest  # Raw file fingerprint, NOT the platform's accepted contract digest.
    code = 0 if report["local_preflight"] == "passed" else 1
    if args.report:
        try:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            with args.report.open("x", encoding="utf-8") as output:
                output.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        except OSError:
            report["report_write_error"] = "Could not create the new report file; choose an unused path. No existing file was overwritten."
            code = 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
