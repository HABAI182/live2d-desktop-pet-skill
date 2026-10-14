#!/usr/bin/env python3
"""Read-only project and Cubism dependency inventory; never an acceptance test."""
import argparse
import json
from pathlib import Path, PureWindowsPath
import subprocess

def command(root, *args):
    try:
        p = subprocess.run(args, cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace')
    except OSError:
        return None
    return p.stdout.strip() if p.returncode == 0 else None

def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8-sig'))
    except (OSError, ValueError):
        return None

def model_inventory(root, relative):
    root = Path(root).resolve()
    if not isinstance(relative, str) or PureWindowsPath(relative).drive or '://' in relative:
        return {'entry': relative, 'error': 'Invalid or absolute model path', 'fileDependenciesVerified': False}
    model = (root / relative).resolve()
    if not model.is_relative_to(root):
        return {'entry': relative, 'error': 'Model path outside project', 'fileDependenciesVerified': False}
    data = read_json(model)
    if not isinstance(data, dict):
        return {'entry': relative, 'error': 'Missing, invalid or non-object JSON', 'fileDependenciesVerified': False}
    refs = data.get('FileReferences', {})
    if not isinstance(refs, dict):
        return {'entry': relative, 'error': 'FileReferences must be an object', 'fileDependenciesVerified': False}
    files = []
    errors = []
    if not isinstance(refs.get('Moc'), str) or not refs.get('Moc'):
        errors.append('Moc must name an exported moc3 file')
    for key in ('Moc', 'Physics', 'Pose', 'UserData', 'DisplayInfo'):
        if refs.get(key):
            if isinstance(refs[key], str):
                files.append(refs[key])
            else:
                errors.append(key+' must be a string')
    textures = refs.get('Textures')
    if not isinstance(textures, list) or not textures or not all(isinstance(x, str) and x for x in textures):
        errors.append('Textures must be a nonempty array of file names')
    else:
        files.extend(textures)

    def add_entries(entries, field):
        if not isinstance(entries, list):
            errors.append(field+' must be an array')
            return
        for entry in entries:
            if isinstance(entry, dict) and isinstance(entry.get('File'), str) and entry['File']:
                files.append(entry['File'])
            else:
                errors.append(field+' entry must have a File string')

    add_entries(refs.get('Expressions', []), 'Expressions')
    motions = refs.get('Motions', {})
    if isinstance(motions, dict):
        for group, entries in motions.items():
            add_entries(entries, 'Motions.'+group)
    else:
        errors.append('Motions must be an object')
    missing, outside = [], []
    for relative_file in sorted(set(files)):
        if PureWindowsPath(relative_file).drive or '://' in relative_file:
            outside.append(relative_file)
            continue
        resolved = (model.parent / relative_file).resolve()
        if not resolved.is_relative_to(root):
            outside.append(relative_file)
        elif not resolved.is_file():
            missing.append(relative_file)
    return {'entry': relative, 'referenceCount': len(set(files)), 'missing': missing,
            'outsideProject': outside, 'schemaErrors': errors, 'fileDependenciesVerified': not missing and not outside and not errors,
            'webglRendered': 'unknown', 'nativeDesktopVerified': 'unknown'}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project', type=Path)
    ap.add_argument('--model', help='Project-relative model3 entry; defaults to tracked model3 files')
    args = ap.parse_args()
    root = args.project.resolve(strict=True)
    if not root.is_dir():
        ap.error('project must be a directory')
    tracked = command(root, 'git', '-c', 'core.quotepath=false', 'ls-files', '-z')
    files = [x for x in tracked.split('\0') if x] if tracked is not None else []
    entries = [args.model] if args.model else [x for x in files if x.endswith('.model3.json')]
    package = read_json(root / 'package.json') or {}
    if not isinstance(package, dict):
        package = {}
    ancestors = [root, *list(root.parents)[:5]]
    result = {
        'project': str(root), 'name': package.get('name'), 'version': package.get('version'),
        'agents': [str(x / 'AGENTS.md') for x in ancestors if (x / 'AGENTS.md').is_file()],
        'commit': command(root, 'git', 'rev-parse', '--short', 'HEAD'),
        'status': command(root, 'git', 'status', '--short'),
        'recentCommits': command(root, 'git', 'log', '-5', '--oneline'),
        'tauri': (root / 'src-tauri').is_dir(),
        'modelDiscovery': 'explicit --model' if args.model else 'Git tracked files only; use --model outside Git',
        'models': [model_inventory(root, x) for x in entries[:20]],
        'editableRigs': [x for x in files if x.endswith('.cmo3')],
        'evidenceScope': 'Files and Git only; visual and native acceptance require separate evidence',
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
