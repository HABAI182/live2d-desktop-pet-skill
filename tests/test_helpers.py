"""Behavior checks for the shipped helpers; no SDK or production app needed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT/'skills/live2d-desktop-pet/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


keyboard = load('keyboard_layout')
inventory = load('inspect_pet')
delivery = load('verify_delivery')


class KeyboardTests(unittest.TestCase):
    def test_facing_pet_reverses_both_axes(self):
        keys = {k['code']: k for k in keyboard.layout()['keys']}
        self.assertGreater(keys['KeyQ']['screen']['x'], keys['KeyP']['screen']['x'])
        self.assertLess(keys['Space']['screen']['y'], keys['Digit1']['screen']['y'])
        self.assertEqual(keys['KeyT']['physical']['side'], 'left')
        self.assertEqual(keys['KeyY']['physical']['side'], 'right')
        self.assertEqual(keys['KeyA']['zone'], 'left-front')
        self.assertEqual(keys['KeyU']['zone'], 'right-back')

    def test_typing_view_has_opposite_projection(self):
        keys = {k['code']: k for k in keyboard.layout('typing-view')['keys']}
        self.assertLess(keys['KeyQ']['screen']['x'], keys['KeyP']['screen']['x'])
        self.assertGreater(keys['Space']['screen']['y'], keys['Digit1']['screen']['y'])

    def test_real_key_shapes_and_complete_letter_coverage(self):
        data = keyboard.layout()
        self.assertEqual(len(data['keys']), 61)
        self.assertEqual(len({k['code'] for k in data['keys']}), 61)
        self.assertEqual({k['label'] for k in data['keys'] if k['code'].startswith('Key')}, set('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        spaces = [k for k in data['keys'] if k['code'] == 'Space']
        self.assertEqual(len(spaces), 1)
        self.assertEqual(spaces[0]['units'], 6.25)
        self.assertEqual(next(k for k in data['keys'] if k['code'] == 'Enter')['units'], 2.25)
        ET.fromstring(keyboard.svg(data))

    def test_cli_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)/'new-reference'
            command = [sys.executable, str(SCRIPTS/'keyboard_layout.py'), '--output-dir', str(output)]
            first = subprocess.run(command, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            saved = (output/'keyboard.svg').read_bytes()
            second = subprocess.run(command, capture_output=True)
            self.assertEqual(second.returncode, 2)
            self.assertEqual((output/'keyboard.svg').read_bytes(), saved)


class FileTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.project = self.base/'project'
        self.project.mkdir()

    def model(self, data, name='pet.model3.json'):
        (self.project/name).write_text(json.dumps(data), encoding='utf-8')
        return inventory.model_inventory(self.project, name)

    def test_reference_check_does_not_claim_runtime(self):
        (self.project/'pet.moc3').write_bytes(b'file-check-fixture-not-a-real-moc')
        (self.project/'texture.png').write_bytes(b'file-check-fixture')
        result = self.model({'Version': 3, 'FileReferences': {'Moc': 'pet.moc3', 'Textures': ['texture.png']}})
        self.assertTrue(result['fileDependenciesVerified'])
        self.assertEqual(result['webglRendered'], 'unknown')
        self.assertEqual(result['nativeDesktopVerified'], 'unknown')

    def test_invalid_types_report_failure_without_traceback(self):
        for data in ([], {'FileReferences': []}, {'FileReferences': {'Moc': 9, 'Textures': 'texture.png', 'Motions': []}}):
            with self.subTest(data=data):
                self.assertFalse(self.model(data)['fileDependenciesVerified'])

    def test_outside_or_missing_dependency_is_not_success(self):
        (self.base/'outside.png').write_bytes(b'outside')
        result = self.model({'FileReferences': {'Moc': 'missing.moc3', 'Textures': ['../outside.png']}})
        self.assertEqual(result['missing'], ['missing.moc3'])
        self.assertEqual(result['outsideProject'], ['../outside.png'])
        self.assertFalse(result['fileDependenciesVerified'])

    def test_cross_platform_absolute_model_is_rejected(self):
        self.assertFalse(inventory.model_inventory(self.project, 'C:/outside/pet.model3.json')['fileDependenciesVerified'])

    def test_git_unicode_filename_round_trip(self):
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True)
        name = '模型 甲.model3.json'
        self.model({'FileReferences': {'Moc': 'pet.moc3', 'Textures': ['texture.png']}}, name)
        subprocess.run(['git', 'add', '--', name], cwd=self.project, check=True)
        run = subprocess.run([sys.executable, str(SCRIPTS/'inspect_pet.py'), str(self.project)], capture_output=True, text=True, encoding='utf-8', check=True)
        result = json.loads(run.stdout)
        self.assertEqual(result['models'][0]['entry'], name)
        self.assertFalse(result['models'][0]['fileDependenciesVerified'])

    def manifest(self, data):
        path = self.project/'SHA256.json'
        path.write_text(json.dumps(data), encoding='utf-8')
        return path

    def test_manifest_formats_and_mismatch(self):
        artifact = self.project/'pet.bin'
        artifact.write_bytes(b'first build')
        row = {'file': artifact.name, 'bytes': artifact.stat().st_size, 'sha256': hashlib.sha256(artifact.read_bytes()).hexdigest()}
        for data in ([row], {'files': [row]}, {'assets': [row]}):
            with self.subTest(data=data):
                result = delivery.verify(self.project, self.manifest(data))
                self.assertTrue(result['filesVerified'])
                self.assertEqual(result['runtimeVerified'], 'unknown')
        artifact.write_bytes(b'changed build')
        self.assertFalse(delivery.verify(self.project, self.manifest([row]))['filesVerified'])

    def test_manifest_rejects_escape_duplicate_and_bad_schema(self):
        base = {'file': 'pet.bin', 'sha256': 'a'*64}
        for data in ([{**base, 'file': '../private.bin'}], [{**base, 'file': 'C:/private.bin'}],
                     [base, base], [None], [], [{'file': 'pet.bin', 'sha256': 'invalid'}]):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    delivery.verify(self.project, self.manifest(data))

    def test_manifest_cli_fails_for_missing_file(self):
        path = self.manifest([{'file': 'not-present.bin', 'sha256': 'a'*64}])
        run = subprocess.run([sys.executable, str(SCRIPTS/'verify_delivery.py'), str(self.project), str(path)], capture_output=True)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(json.loads(run.stdout)['filesVerified'])


if __name__ == '__main__':
    unittest.main()
