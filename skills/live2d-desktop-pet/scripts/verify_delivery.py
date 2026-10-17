#!/usr/bin/env python3
"""Read-only file size/SHA256 verification; not runtime or signing acceptance."""
import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re
import sys


def verify(directory, manifest):
    root = Path(directory).resolve(strict=True)
    data = json.loads(Path(manifest).read_text(encoding='utf-8-sig'))
    rows = data if isinstance(data, list) else next((data[k] for k in ('files', 'assets') if k in data), None) if isinstance(data, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError('expected a nonempty list, files array or assets array')
    result, seen = [], set()
    for item in rows:
        if not isinstance(item, dict):
            raise ValueError('manifest row is not an object')
        name = item.get('file')
        if not isinstance(name, str) or not name or Path(name).is_absolute() or PureWindowsPath(name).drive:
            raise ValueError('invalid or absolute artifact path')
        target = (root/name).resolve()
        if not target.is_relative_to(root):
            raise ValueError('artifact path outside delivery directory')
        if target in seen:
            raise ValueError('duplicate artifact path')
        seen.add(target)
        digest = item.get('sha256')
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-fA-F]{64}', digest):
            raise ValueError('invalid SHA256 value')
        expected_size = item.get('bytes')
        if expected_size is not None and (type(expected_size) is not int or expected_size < 0):
            raise ValueError('invalid artifact size')
        try:
            actual_size = target.stat().st_size
            hasher = hashlib.sha256()
            with target.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024*1024), b''):
                    hasher.update(chunk)
            actual_digest = hasher.hexdigest().upper()
            passed = actual_digest == digest.upper() and (expected_size is None or actual_size == expected_size)
            result.append({'file': name, 'passed': passed, 'bytes': actual_size, 'sha256': actual_digest})
        except OSError as error:
            result.append({'file': name, 'passed': False, 'error': str(error)})
    return {'filesVerified': all(x['passed'] for x in result), 'artifacts': result,
            'runtimeVerified': 'unknown', 'signatureVerified': 'unknown',
            'scope': 'Local files only; no upload, deletion, execution or OS acceptance'}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        report = verify(args.directory, args.manifest)
    except (ValueError, OSError) as error:
        print(json.dumps({'filesVerified': False, 'error': str(error)}))
        raise SystemExit(2)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['filesVerified'] else 1)


if __name__ == '__main__':
    main()
