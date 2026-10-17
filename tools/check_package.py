"""Validate shipped JSON, local Markdown links and grandfathered asset hashes."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
HASHES = {
    'changli-composition-reference.jpg': 'fc87ea0cac9a3c283529585ec52a3909c9149e74c3ba1502d006ac817e132c11',
    'xuanling-base-reference.png': 'f620733c7bdc692948611f4c4139227747a64001d77a1ed807a2a16580d2d5d8',
}


def main():
    files = [p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts]
    for path in files:
        if path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8-sig'))
        if path.suffix == '.md':
            for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', path.read_text(encoding='utf-8')):
                target = unquote(target.split('#', 1)[0])
                if target and ':' not in target:
                    resolved = (path.parent / target).resolve()
                    if not resolved.is_relative_to(ROOT) or not resolved.exists():
                        raise ValueError(f'Broken local link: {path.relative_to(ROOT)} -> {target}')
    for name, expected in HASHES.items():
        path = ROOT / 'skills/live2d-desktop-pet/assets' / name
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Example asset changed without provenance review: {name}')
    print('Shipped JSON, local Markdown links and 2 example asset hashes verified; rights remain permission-pending.')


if __name__ == '__main__':
    main()
