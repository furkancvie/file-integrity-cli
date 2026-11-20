import argparse
import hashlib
import json
from pathlib import Path


def snapshot(root, exclude=None):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('Root must be a directory')
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink() or not path.is_file() or path.resolve() == exclude:
            continue
        with path.open('rb') as stream:
            digest = hashlib.sha256()
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
            result[path.relative_to(root).as_posix()] = digest.hexdigest()
    return result


def compare(expected, actual):
    return {'missing': sorted(expected.keys() - actual.keys()),
            'added': sorted(actual.keys() - expected.keys()),
            'changed': sorted(k for k in expected.keys() & actual.keys() if expected[k] != actual[k])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['create', 'verify'])
    parser.add_argument('directory', type=Path)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        actual = snapshot(args.directory, args.manifest.resolve())
        if args.action == 'create':
            with args.manifest.open('x', encoding='utf-8') as f:
                json.dump(actual, f, indent=2, sort_keys=True)
            return 0
        expected = json.loads(args.manifest.read_text(encoding='utf-8'))
        if not isinstance(expected, dict) or not all(isinstance(v, str) for v in expected.values()):
            raise ValueError('Invalid manifest')
        report = compare(expected, actual)
        print(json.dumps(report, indent=2))
        return int(any(report.values()))
    except (ValueError, OSError) as exc:
        parser.exit(2, f'{exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
