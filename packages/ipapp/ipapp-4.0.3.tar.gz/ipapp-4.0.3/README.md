# ipapp • v4.0.3

Tiny **stdlib-only** client for [ip.app](https://ip.app). No dependencies on third party packages.
Query your public IP address, ASN data, location, timezone, and more — programmatically *or* from the command line.

---

## 🛠 Installation

```bash
# From PyPI: https://pypi.org/project/ipapp/
pip install ipapp
```

Python ≥ 3.8, no external runtime dependencies.

### Using a virtual environment (recommended)

If your system Python is *externally managed* (PEP 668) you’ll need an isolated environment instead of installing into the OS packages. The fastest path is a **virtual env**:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e '.[dev]'
```

(Upgrade `pip` inside the venv if you like: `python -m pip install --upgrade pip`.)

Alternatively you can keep things completely separate with **pipx**:

```bash
# From PyPI: https://pypi.org/project/ipapp/
pipx install ipapp
```

---

## 🚀 Quick-start (Python)

Each endpoint gets its own snippet so you can copy/paste exactly what you need.

### Public IP

```python
import ipapp
print(ipapp.get_ip())          # → "203.0.113.42"
```

### Public IP via HEAD (fastest)
```python
import ipapp
print(ipapp.get_ip(head=True))     # "203.0.113.42" via X-Ipapp-Ip header
```

### ASN (plain-text)

```python
import ipapp
print(ipapp.get_asn())         # → "AS12345"
```

### ASN (JSON)

```python
import ipapp
info = ipapp.get_asn(json=True)
# {'asn': 12345, 'holder': 'Example ISP', 'country': 'DE', ...}
```

### ASN with caller IP merged (JSON only)

```python
import ipapp
info = ipapp.get_asn(json=True, include_ip=True)
# {'asn': 12345, 'holder': 'Example ISP', ..., 'ip': '203.0.113.42', 'ip_version': '4'}
```

### Timezone (plain-text)

```python
import ipapp
print(ipapp.get_tz())          # → "Europe/Berlin"
```

### Timezone (JSON)

```python
import ipapp
info = ipapp.get_tz(json=True)
# {'tz': 'Europe/Berlin', ...}
```

### Timezone with caller IP merged (JSON only)

```python
import ipapp
info = ipapp.get_tz(json=True, include_ip=True)
# {'tz': 'Europe/Berlin', 'ip': '203.0.113.42', 'ip_version': '4'}
```

### Location (JSON)

```python
import ipapp
info = ipapp.get_location()    # JSON by default
# {'city': 'Berlin', 'country': 'DE', 'region': 'Berlin', ...}
```

### Location with caller IP merged (JSON only)

```python
import ipapp
info = ipapp.get_location(include_ip=True)
# {'city': 'Berlin', 'country': 'DE', ..., 'ip': '203.0.113.42', 'ip_version': '4'}
```

### Location (plain-text)

```python
import ipapp
print(ipapp.get_location(json=False))  # raw plain-text response
```

All helpers raise `ipapp.IPAppError` on network problems or invalid responses.

### Strict mode

All functions support a `strict=True` parameter that raises `IPAppError` instead of returning `None` when the service responds with "Unknown":

```python
import ipapp
try:
    ip = ipapp.get_ip(strict=True)
except ipapp.IPAppError:
    print("IP address is unknown")
```

---

## 🖥 Quick-start (CLI)

Every function is mirrored by a sub-command.
No arguments prints the IP (nice for scripts):

```bash
ipapp                        # 198.51.100.7
```

Run each endpoint separately:

```bash
ipapp ip                     # same as default
ipapp ip --json              # {"ip": "198.51.100.7"}
ipapp ip --head              # header-only mode

ipapp asn                    # AS12345
ipapp asn --json             # {"asn": 12345, ...}
ipapp asn --json --include-ip # {"asn": 12345, ..., "ip": "198.51.100.7"}

ipapp tz                     # Europe/Berlin
ipapp tz --json              # {"tz": "Europe/Berlin", ...}
ipapp tz --json --include-ip # {"tz": "Europe/Berlin", "ip": "198.51.100.7"}

ipapp location               # {"city": "Berlin", "country": "DE", ...}
ipapp location --include-ip  # {"city": "Berlin", ..., "ip": "198.51.100.7"}
ipapp location --head        # header-only mode
```

---

## 🧪 Running the test suite

Tests are network-free (they monkey-patch the internal fetcher) so they run instantly:

```bash
pytest -q
# 4 passed in 0.02s
```

---

## 📦 Building & checking the package

```bash
# Ensure build tools are present
pipx install build twine

# Remove old version
rm -rf dist/*

# Build wheel + sdist into ./dist/
pyproject-build

# Verify metadata is valid (no upload)
twine check dist/*

# When you're ready to release
twine upload dist/*
```

Wait a few minutes and test by reinstalling using pipx:

```bash
pipx reinstall ipapp
```

---

## 🤝 Contributing

* Fork, create a feature branch, add tests for any new behaviour.
* Keep code **PEP 8** compliant (the codebase sticks to stdlib only).
* Open a PR – CI will run `pytest` and basic metadata checks.

---

## 🔗 Links

- **PyPI**: https://pypi.org/project/ipapp/
- **GitHub**: https://github.com/fili/ipapp-client
- **IP.app API**: https://ip.app
- **IP.app API Documentation**: https://github.com/fili/ipapp

---

> Note: Versioning starts at 4.0.0 to avoid conflicts with a previously removed package on PyPI using the same name.

MIT licensed – have fun!
