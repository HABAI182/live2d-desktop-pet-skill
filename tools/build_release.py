"""Build a reproducible installable skill from tracked blobs at one Git commit."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = 'live2d-desktop-pet'
PREFIX = f'skills/{SKILL}/'


def git(*args, root=ROOT):
    return subprocess.check_output(['git', '-C', str(root), *args])


def release_payload(root=ROOT, ref='HEAD', expected_tag=None):
    commit = git('rev-parse', '--verify', ref + '^{commit}', root=root).decode().strip()
    def blob(path):
        return git('show', f'{commit}:{path}', root=root)
    version = blob('VERSION').decode().strip()
    if not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', version):
        raise ValueError('VERSION must contain a stable major.minor.patch version')
    if expected_tag is not None and expected_tag != 'v' + version:
        raise ValueError('Tag does not match VERSION')
    entry = blob(PREFIX + 'SKILL.md').decode('utf-8')
    frontmatter = entry.split('---', 2)[1] if entry.startswith('---\n') else ''
    match = re.search(r'^\s+version:\s*["\']?([\d.]+)["\']?\s*$', frontmatter, re.M)
    if not match or match[1] != version:
        raise ValueError('Skill metadata version does not match VERSION')
    names = git('ls-tree', '-r', '--name-only', '-z', commit, '--', PREFIX, root=root).decode().strip('\0').split('\0')
    payload = {}
    for name in names:
        relative = Path(name[len(PREFIX):])
        if not name.startswith(PREFIX) or relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe skill path')
        if any(p.startswith('.') or p == '__pycache__' for p in relative.parts) or relative.suffix == '.pyc':
            raise ValueError('Local/generated files must not be tracked in the skill')
        if relative.parts[0] == 'assets' and relative.as_posix() != 'assets/ASSET-NOTICE.md':
            raise ValueError('Review provenance before adding skill assets')
        payload[f'{SKILL}/{relative.as_posix()}'] = blob(name)
    payload[f'{SKILL}/LICENSE'] = blob('LICENSE')
    payload[f'{SKILL}/VERSION'] = (version + '\n').encode()
    changelog = blob('CHANGELOG.md').decode('utf-8')
    marker = f'## v{version} — '
    if marker not in changelog:
        raise ValueError('Missing release section in CHANGELOG.md')
    notes = changelog.split(marker, 1)[1].split('\n', 1)[1].split('\n## ', 1)[0].strip()
    return commit, version, payload, notes


def make_archive(payload):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(payload.items()):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    return output.getvalue()


def build(output_dir, root=ROOT, ref='HEAD', expected_tag=None):
    commit, version, payload, notes = release_payload(root, ref, expected_tag)
    archive = make_archive(payload)
    stem = f'live2d-desktop-pet-skill-v{version}'
    manifest = {'version': version, 'source_commit': commit, 'files': []}
    files = {stem + '.zip': archive, stem + '.skill': archive}
    for name, content in files.items():
        manifest['files'].append({'file': name, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest()})
    files[f'SHA256-v{version}.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    files['RELEASE-NOTES.md'] = (f'# v{version}\n\n{notes}\n\n'
        f'解压 ZIP 或 .skill（同内容 ZIP 格式），将 `{SKILL}` 文件夹放入 `~/.codex/skills/`。'
        '`.skill` 不要求 Codex 支持直接导入；按普通 ZIP 解压即可。\n\n'
        '包含技能说明、参考、脚本、模板、MIT LICENSE 与版本号；不包含角色位图、模型、SDK/Core 或私人素材。\n\n'
        f'源码 commit：`{commit}`。附件已从该提交的跟踪文件构建；SHA256 清单用于下载核对。\n').encode('utf-8')
    output_dir = Path(output_dir)
    if any((output_dir / name).exists() for name in files):
        raise FileExistsError('Release output exists; use a new output directory')
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (output_dir / name).write_bytes(content)
    verify(output_dir, root, ref, expected_tag)
    return manifest


def verify(directory, root=ROOT, ref='HEAD', expected_tag=None):
    commit, version, payload, _ = release_payload(root, ref, expected_tag)
    directory = Path(directory)
    manifest = json.loads((directory / f'SHA256-v{version}.json').read_text(encoding='utf-8'))
    if manifest['version'] != version or manifest['source_commit'] != commit:
        raise ValueError('Manifest source/version mismatch')
    expected = {f'live2d-desktop-pet-skill-v{version}{ext}' for ext in ['.zip', '.skill']}
    if len(manifest['files']) != 2 or {r['file'] for r in manifest['files']} != expected:
        raise ValueError('Manifest must contain exactly the ZIP and skill package')
    allowed = expected | {f'SHA256-v{version}.json', 'RELEASE-NOTES.md'}
    if {p.name for p in directory.iterdir()} - allowed:
        raise ValueError('Unexpected release download files')
    for row in manifest['files']:
        content = (directory / row['file']).read_bytes()
        if len(content) != row['bytes'] or hashlib.sha256(content).hexdigest() != row['sha256']:
            raise ValueError('Archive checksum mismatch')
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            if archive.testzip() is not None or len(archive.namelist()) != len(payload) or set(archive.namelist()) != set(payload):
                raise ValueError('Archive paths or CRC differ from source')
            if any(archive.read(name) != blob for name, blob in payload.items()):
                raise ValueError('Archive bytes differ from tracked source')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    parser.add_argument('--verify-dir', type=Path)
    parser.add_argument('--ref', default='HEAD')
    parser.add_argument('--expected-tag')
    args = parser.parse_args()
    result = verify(args.verify_dir, ref=args.ref, expected_tag=args.expected_tag) if args.verify_dir else build(args.output_dir, ref=args.ref, expected_tag=args.expected_tag)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
