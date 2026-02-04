#!/usr/bin/env python3
"""Upload a file to JFrog Artifactory (generic repository) using HTTP PUT."""

import argparse
import os
import base64
import urllib.request
import urllib.error


def put_file(url: str, file_path: str, username: str, password: str) -> int:
    with open(file_path, 'rb') as f:
        data = f.read()

    # Use URL as-is but add matrix parameters for Artifactory
    final_url = f"{url};charset=UTF-8"
    req = urllib.request.Request(final_url, data=data, method='PUT')
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    req.add_header('Authorization', f'Basic {token}')
    req.add_header('Content-Type', 'application/octet-stream')

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Upload OK: HTTP {resp.status}")
            return 0
    except urllib.error.HTTPError as e:
        print(f"Upload failed: HTTP {e.code} {e.reason}")
        body = e.read().decode('utf-8', errors='ignore')
        if body:
            print(body)
        return 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', required=True)
    p.add_argument('--repo', required=True)
    p.add_argument('--file', required=True)
    p.add_argument('--target-path', required=True)
    p.add_argument('--username', required=True)
    p.add_argument('--password', required=True)
    args = p.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}")
        return 2

    base = args.base_url.rstrip('/')
    url = f"{base}/{args.repo}/{args.target_path.lstrip('/')}"
    print(f"Uploading to: {url}")
    return put_file(url, args.file, args.username, args.password)


if __name__ == '__main__':
    raise SystemExit(main())
