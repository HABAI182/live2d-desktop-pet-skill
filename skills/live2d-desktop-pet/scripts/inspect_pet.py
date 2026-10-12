#!/usr/bin/env python3
"""Read-only project and Cubism dependency inventory; never an acceptance test."""
import argparse
import json
from pathlib import Path
import subprocess

def command(root, *args):
    p = subprocess.run(args, cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return p.stdout.strip() if p.returncode == 0 else None

def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except (OSError, ValueError):
        return None

def model_inventory(root, relative):
    model = (root / relative).resolve()
    if not model.is_relative_to(root):
        return {'entry': relative, 'error': 'Model path outside project'}
    data = read_json(model)
    if not data:
        return {'entry': relative, 'error': 'Missing or invalid JSON'}
    refs = data.get('FileReferences', {})
    files = []
    for key in ('Moc', 'Physics', 'Pose', 'UserData', 'DisplayInfo'):
        if refs.get(key):
            files.append(refs[key])
    files.extend(refs.get('Textures', []))
    files.extend(x['File'] for x in refs.get('Expressions', []) if x.get('File'))
    for motions in refs.get('Motions', {}).values():
        files.extend(x['File'] for x in motions if x.get('File'))
    missing, outside = [], []
    for relative_file in sorted(set(files)):
        resolved = (model.parent / relative_file).resolve()
        if not resolved.is_relative_to(root):
            outside.append(relative_file)
        elif not resolved.is_file():
            missing.append(relative_file)
    return {'entry': relative, 'referenceCount': len(set(files)), 'missing': missing,
            'outsideProject': outside, 'fileDependenciesVerified': not missing and not outside,
            'webglRendered': 'unknown', 'nativeDesktopVerified': 'unknown'}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project', type=Path)
    ap.add_argument('--model', help='Project-relative model3 entry; defaults to tracked model3 files')
    args = ap.parse_args()
    root = args.project.resolve(strict=True)
    if not root.is_dir():
        ap.error('project must be a directory')
    tracked = command(root, 'git', 'ls-files')
    files = tracked.splitlines() if tracked is not None else []
    entries = [args.model] if args.model else [x for x in files if x.endswith('.model3.json')]
    package = read_json(root / 'package.json') or {}
    ancestors = [root, *list(root.parents)[:5]]
    result = {
        'project': str(root), 'name': package.get('name'), 'version': package.get('version'),
        'agents': [str(x / 'AGENTS.md') for x in ancestors if (x / 'AGENTS.md').is_file()],
        'commit': command(root, 'git', 'rev-parse', '--short', 'HEAD'),
        'status': command(root, 'git', 'status', '--short'),
        'recentCommits': command(root, 'git', 'log', '-5', '--oneline'),
        'tauri': (root / 'src-tauri').is_dir(),
        'models': [model_inventory(root, x) for x in entries[:20]],
        'editableRigs': [x for x in files if x.endswith('.cmo3')],
        'evidenceScope': 'Files and Git only; visual and native acceptance require separate evidence',
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
