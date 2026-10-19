"""Exercise release integrity against an isolated tracked Git source."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location('release_builder', Path(__file__).resolve().parents[1] / 'tools/build_release.py')
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.name', 'release-test')
        self.git('config', 'user.email', 'test@example.invalid')
        entry = self.source / 'skills/live2d-desktop-pet/SKILL.md'
        entry.parent.mkdir(parents=True)
        entry.write_text('---\nname: live2d-desktop-pet\ndescription: Test fixture\nmetadata:\n  version: "1.2.3"\n---\n\nTest\n', encoding='utf-8')
        (self.source / 'VERSION').write_text('1.2.3\n', encoding='utf-8')
        (self.source / 'LICENSE').write_text('MIT fixture\n', encoding='utf-8')
        (self.source / 'CHANGELOG.md').write_text('# Changes\n\n## v1.2.3 — test\n\n- Release fixture\n', encoding='utf-8')
        self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.source), *args], stderr=subprocess.STDOUT)

    def commit(self):
        self.git('add', '--all')
        self.git('commit', '-qm', 'fixture')

    def test_reproducible_install_package_excludes_untracked_files(self):
        (self.source / 'skills/live2d-desktop-pet/.env').write_text('private', encoding='utf-8')
        (self.source / 'skills/live2d-desktop-pet/private.png').write_bytes(b'untracked')
        first = release.build(self.root / 'first', self.source, expected_tag='v1.2.3')
        second = release.build(self.root / 'second', self.source, expected_tag='v1.2.3')
        self.assertEqual(first, second)
        one = self.root / 'first' / first['files'][0]['file']
        two = self.root / 'second' / second['files'][0]['file']
        self.assertEqual(one.read_bytes(), two.read_bytes())
        with zipfile.ZipFile(one) as archive:
            self.assertEqual(set(archive.namelist()), {'live2d-desktop-pet/SKILL.md', 'live2d-desktop-pet/VERSION', 'live2d-desktop-pet/LICENSE'})
            self.assertEqual(archive.read('live2d-desktop-pet/SKILL.md'), self.git('show', 'HEAD:skills/live2d-desktop-pet/SKILL.md'))

    def test_tag_must_match_version(self):
        with self.assertRaisesRegex(ValueError, 'Tag does not match'):
            release.build(self.root / 'out', self.source, expected_tag='v9.9.9')

    def test_metadata_version_skew_fails(self):
        (self.source / 'VERSION').write_text('1.2.4\n', encoding='utf-8')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'metadata version'):
            release.build(self.root / 'out', self.source)

    def test_unreviewed_tracked_asset_fails(self):
        assets = self.source / 'skills/live2d-desktop-pet/assets'
        assets.mkdir()
        (assets / 'private.png').write_bytes(b'tracked raster')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'provenance'):
            release.build(self.root / 'out', self.source)

    def test_existing_release_output_is_not_overwritten(self):
        release.build(self.root / 'out', self.source)
        with self.assertRaises(FileExistsError):
            release.build(self.root / 'out', self.source)

    def test_unexpected_download_asset_fails(self):
        out = self.root / 'out'
        release.build(out, self.source)
        (out / 'private-model.cmo3').write_bytes(b'not a release asset')
        with self.assertRaisesRegex(ValueError, 'Unexpected release'):
            release.verify(out, self.source)

    def test_injected_archive_file_fails_even_with_updated_checksum(self):
        out = self.root / 'out'
        manifest = release.build(out, self.source)
        row = manifest['files'][0]
        with zipfile.ZipFile(out / row['file'], 'a') as archive:
            archive.writestr('private.cmo3', b'should never ship')
        data = (out / row['file']).read_bytes()
        row.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        (out / 'SHA256-v1.2.3.json').write_text(json.dumps(manifest), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Archive paths'):
            release.verify(out, self.source)


if __name__ == '__main__':
    unittest.main()
