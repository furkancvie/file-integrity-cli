# File Integrity CLI

Create SHA-256 manifests and verify changed, missing and unexpected files.

## Requirements

Python 3.10 or newer. No third-party dependencies.

## Usage

```bash
python app.py create ./folder manifest.json
python app.py verify ./folder manifest.json
```

## Tests

```bash
python -m unittest discover -v
```

## Limitations

Keep the manifest in a trusted location. This detects differences, not authenticity. Symlink files are skipped; verification returns 1 for differences and 2 for errors. Creation refuses to overwrite an existing manifest.

## License

MIT.
