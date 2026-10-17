"""Validate shipped JSON, local Markdown links and the asset-free package scope."""
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]



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
    assets = ROOT / 'skills/live2d-desktop-pet/assets'
    if {p.name for p in assets.iterdir()} != {'ASSET-NOTICE.md'}:
        raise ValueError('Review provenance and update the asset policy before shipping examples')
    print('Shipped JSON, local Markdown links and absence of unlicensed raster examples verified.')


if __name__ == '__main__':
    main()
