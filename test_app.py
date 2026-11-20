import tempfile
import unittest
from pathlib import Path
from app import snapshot, compare

class Tests(unittest.TestCase):
    def test_empty(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(snapshot(d), {})
    def test_known_hash(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'a').write_bytes(b'abc')
            self.assertEqual(snapshot(d)['a'], 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
    def test_changes(self):
        self.assertEqual(compare({'a':'1','b':'2'}, {'a':'3','c':'4'}), {'missing':['b'],'added':['c'],'changed':['a']})
    def test_same(self):
        self.assertFalse(any(compare({'a':'1'}, {'a':'1'}).values()))
    def test_exclude_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'manifest.json'; p.write_text('{}')
            self.assertEqual(snapshot(d,p.resolve()), {})
    def test_missing_root(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): snapshot(Path(d)/'absent')
