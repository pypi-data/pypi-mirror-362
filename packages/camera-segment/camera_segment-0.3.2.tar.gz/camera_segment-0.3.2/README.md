# camera-segment

**A Python tool to capture segments of video from cameras.**

---

## 🚀 What it does

**`camera-segment`** is a Python package and CLI tool designed to help you capture and save segments of video from one or more cameras. (Implementation coming soon!)

**Planned Features:**
- 🎥 Capture video segments from local or network cameras
- ⏱️ Specify start/end times or durations
- 💾 Save segments to disk in standard formats
- 🛠️ Command-line interface for automation
- 📦 Python API for integration in your own scripts

---

## 📦 Install

```bash
pip install camera-segment --upgrade
```

---

## 🛠️ Usage

> **Note:** The CLI and API are not yet implemented. Example usage will be added in a future release.

```bash
# Example (coming soon):
camera-segment record --camera 0 --start 00:01:00 --duration 00:00:30 --output segment.mp4
```

---

## 🧹 Local development

The project includes a simple `Makefile`:

```bash
make setup     # create venv and install editable package
make lint      # check for lint issues
make format    # automatically reformat code
make test      # run unittest
make coverage  # collect and display code coverage stats
make clean     # remove build artifacts
```

---

## 🚦 CI & Release

- Automated linting, testing, and build checks via GitHub Actions
- Release automation with [release-please](https://github.com/googleapis/release-please)
- Publish to PyPI using Trusted Publishers

### Manual Release Tagging

If you need to deploy a release that doesn't include a `fix`, `feat`, or `docs` commit (for example, a pure chore or meta change), you can manually trigger a release with:

```bash
git commit --allow-empty -m "chore: release 0.3.1 (manual)" -m "Release-As: 0.3.1"
```

Replace `0.3.1` with the desired version number.

---

## 📄 Links

- [Homepage](https://github.com/jbussdieker/python-camera-segment)
- [Documentation](https://github.com/jbussdieker/python-camera-segment/blob/main/README.md)
- [Repository](https://github.com/jbussdieker/python-camera-segment)
- [Issues](https://github.com/jbussdieker/python-camera-segment/issues)
- [Changelog](https://github.com/jbussdieker/python-camera-segment/blob/main/CHANGELOG.md)

---

## 📝 License

This project is licensed under **MIT**.

Copyright (c) 2025 Joshua B. Bussdieker
