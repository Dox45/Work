"""A tiny API test sample.

A quick, dependency-free check that outbound HTTP calls work.
Run it with:  python3 sample_api_test.py
"""

import urllib.request

TEST_URL = "https://api.github.com/zen"


def fetch(url, timeout=10):
    """Send a GET request and return (status code, body text)."""
    request = urllib.request.Request(url, headers={"User-Agent": "work-sample-api-test"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read().decode("utf-8")


def main():
    status, body = fetch(TEST_URL)
    print(f"Status: {status}")
    print(f"Body: {body.strip()[:200]}")


if __name__ == "__main__":
    main()
