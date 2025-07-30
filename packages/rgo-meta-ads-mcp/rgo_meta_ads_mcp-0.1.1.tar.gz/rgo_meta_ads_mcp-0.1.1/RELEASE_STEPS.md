# Release Guide for rgo-meta-ads-mcp

This guide outlines the steps to prepare and publish a new release to PyPI.

---

## 1. Update Version

Edit `pyproject.toml` and increment the version number:

```
[project]
version = "NEW_VERSION"
```

---

## 2. Update Changelog/README (Optional)
- Add release notes or update documentation as needed.

---

## 3. Build and Upload (Recommended: Use the Script)

You can automate the build and upload process using the provided `upload.sh` script:

```sh
export PYPI_TOKEN=pypi-<your-token>
./upload.sh
```

This script will:
- Clean previous builds
- Build the package
- Check the package
- Upload to PyPI

---

## 4. Manual Steps (Alternative)

If you prefer to run steps manually:

### Build the Distribution
```sh
python -m build
```

### Check the Distribution (Optional but recommended)
```sh
twine check dist/*
```

### Publish to PyPI
```sh
twine upload dist/* -u __token__ -p pypi-<YOUR-TOKEN>
```

---

## 5. Verify Release
- Visit https://pypi.org/project/rgo-meta-ads-mcp/ to confirm the new version is live.

---

## 6. Clean Up Old Builds (Optional)
```sh
rm -rf dist/ build/ *.egg-info
```

---

## Notes
- Always credit the original author in your documentation.
- For major changes, update the README and THANKS.md as needed.
- For automated releases, consider using GitHub Actions or similar CI/CD tools. 