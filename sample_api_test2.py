"""A second, slightly fuller API test sample.

Dependency-free: only the Python standard library is used.
Run it with:  python3 sample_api_test2.py

It checks the GitHub public API and prints a short pass/fail summary.
"""

import json
import urllib.request

BASE_URL = "https://api.github.com"
TIMEOUT = 10


def fetch_json(path):
    """GET a path from the API and return (status code, parsed body or None)."""
    request = urllib.request.Request(
        BASE_URL + path,
        headers={
            "User-Agent": "work-sample-api-test",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        status = response.status
        raw = response.read().decode("utf-8")
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        body = None
    return status, body


def check_zen():
    """The /zen endpoint should return 200."""
    status, _ = fetch_json("/zen")
    return status == 200, f"GET /zen returned status {status}"


def check_repository():
    """A known public repo should come back with a name and a default branch."""
    status, body = fetch_json("/repos/octocat/Hello-World")
    if status != 200 or not isinstance(body, dict):
        return False, f"GET /repos/octocat/Hello-World returned status {status}"
    if "full_name" not in body:
        return False, "Repository response did not include full_name"
    return True, f"Repository found: {body['full_name']}"


def main():
    tests = [("zen endpoint", check_zen), ("repository lookup", check_repository)]
    passed = 0

    print("Running sample API checks...")
    for name, test in tests:
        try:
            ok, detail = test()
        except Exception as error:  # network or parsing problem
            ok, detail = False, f"error: {error}"
        passed += 1 if ok else 0
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    print(f"\n{passed}/{len(tests)} checks passed")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    raise SystemExit(main())
