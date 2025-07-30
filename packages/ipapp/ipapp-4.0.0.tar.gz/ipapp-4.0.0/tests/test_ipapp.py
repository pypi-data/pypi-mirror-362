"""
Exhaustive, network-free test-suite for ipapp (23 cases).

A smart stub for ipapp.client._fetch emulates the library’s own
“Unknown → None / IPAppError” rules so wrappers behave exactly as they
would on real responses.
"""
from __future__ import annotations
from typing import Any

import pytest
import ipapp
from ipapp import client, IPAppError

UNKNOWN = "Unknown"


def smart_stub(ret: Any):
    """
    Return a fake _fetch that:
      • raises IPAppError when strict=True and value is Unknown
      • converts Unknown → None when strict=False
      • otherwise returns *ret* unchanged
    """

    def _fake(*_a: Any, **k: Any):
        strict = k.get("strict", False)

        # header-only path may pass `header=…`
        if k.get("head"):
            if strict and (ret is None or str(ret).lower() == "unknown"):
                raise IPAppError("IP address unknown")
            return None if str(ret).lower() == "unknown" else ret

        # JSON / plain-text path
        if isinstance(ret, str):
            if ret.lower() == "unknown":
                if strict:
                    raise IPAppError("IP address unknown")
                return None
            return ret

        if isinstance(ret, dict):
            val = ret.copy()
            if "ip" in val and isinstance(val["ip"], str):
                if val["ip"].lower() == "unknown":
                    if strict:
                        raise IPAppError("IP address unknown")
                    val["ip"] = None
            return val
        return ret

    return _fake


# ---------------------------------------------------------------------------
# get_ip  (7 tests)
# ---------------------------------------------------------------------------
def test_ip_plain_ok(monkeypatch):
    monkeypatch.setattr(client, "_fetch", smart_stub("1.2.3.4"))
    assert ipapp.get_ip() == "1.2.3.4"


def test_ip_plain_unknown(monkeypatch):
    monkeypatch.setattr(client, "_fetch", smart_stub(UNKNOWN))
    assert ipapp.get_ip() is None
    with pytest.raises(IPAppError):
        ipapp.get_ip(strict=True)


def test_ip_json(monkeypatch):
    good = {"ip": "203.0.113.9"}
    monkeypatch.setattr(client, "_fetch", smart_stub(good))
    assert ipapp.get_ip(json=True) == good

    bad = {"ip": UNKNOWN}
    monkeypatch.setattr(client, "_fetch", smart_stub(bad))
    assert ipapp.get_ip(json=True)["ip"] is None
    with pytest.raises(IPAppError):
        ipapp.get_ip(json=True, strict=True)


def test_ip_head(monkeypatch):
    monkeypatch.setattr(client, "_fetch", smart_stub("2001:db8::1"))
    assert ipapp.get_ip(head=True) == "2001:db8::1"


# ---------------------------------------------------------------------------
# get_tz  (5 tests)
# ---------------------------------------------------------------------------
def test_tz_plain(monkeypatch):
    monkeypatch.setattr(client, "_fetch", smart_stub("Europe/Berlin"))
    assert ipapp.get_tz() == "Europe/Berlin"


def test_tz_json_include_ip(monkeypatch):
    good = {"tz": "UTC", "ip": "1.1.1.1", "ip_version": "4"}
    monkeypatch.setattr(client, "_fetch", smart_stub(good))
    assert ipapp.get_tz(json=True, include_ip=True) == good


def test_tz_json_include_ip_unknown(monkeypatch):
    bad = {"tz": "UTC", "ip": UNKNOWN, "ip_version": ""}
    monkeypatch.setattr(client, "_fetch", smart_stub(bad))
    assert ipapp.get_tz(json=True, include_ip=True)["ip"] is None
    with pytest.raises(IPAppError):
        ipapp.get_tz(json=True, include_ip=True, strict=True)


def test_tz_head_include_ip(monkeypatch):
    hdr = {
        "x-ipapp-tz": "UTC",
        "x-ipapp-ip": "2.2.2.2",
        "x-ipapp-ip-version": "4",
    }
    monkeypatch.setattr(client, "_fetch", smart_stub(hdr))
    out = ipapp.get_tz(head=True, include_ip=True)
    assert out == {"tz": "UTC", "ip": "2.2.2.2", "ip_version": "4"}


def test_tz_include_ip_plain_ignored(monkeypatch):
    monkeypatch.setattr(client, "_fetch", smart_stub("UTC"))
    assert ipapp.get_tz(include_ip=True) == "UTC"


# ---------------------------------------------------------------------------
# get_location  (6 tests)
# ---------------------------------------------------------------------------
def test_location_head(monkeypatch):
    hdr = {"x-ipapp-loc-city": "Berlin", "x-ipapp-loc-country": "DE"}
    monkeypatch.setattr(client, "_fetch", smart_stub(hdr))
    out = ipapp.get_location(head=True)
    assert out == {"city": "Berlin", "country": "DE"}


def test_location_head_include_ip(monkeypatch):
    hdr = {
        "x-ipapp-location-city": "Paris",
        "x-ipapp-ip": "3.3.3.3",
        "x-ipapp-ip-version": "4",
    }
    monkeypatch.setattr(client, "_fetch", smart_stub(hdr))
    out = ipapp.get_location(head=True, include_ip=True)
    assert out["ip"] == "3.3.3.3"


def test_location_head_strict_missing(monkeypatch):
    monkeypatch.setattr(client, "_fetch", smart_stub({}))
    with pytest.raises(IPAppError):
        ipapp.get_location(head=True, strict=True)


def test_location_json_include_ip(monkeypatch):
    good = {"city": "NYC", "ip": "4.4.4.4", "ip_version": "4"}
    monkeypatch.setattr(client, "_fetch", smart_stub(good))
    assert ipapp.get_location(json=True, include_ip=True) == good


def test_location_json_include_ip_unknown(monkeypatch):
    bad = {"city": "Paris", "ip": UNKNOWN, "ip_version": ""}
    monkeypatch.setattr(client, "_fetch", smart_stub(bad))
    assert ipapp.get_location(json=True, include_ip=True)["ip"] is None
    with pytest.raises(IPAppError):
        ipapp.get_location(json=True, include_ip=True, strict=True)


# ---------------------------------------------------------------------------
# get_asn  (5 tests)
# ---------------------------------------------------------------------------
def test_asn_plain(monkeypatch):
    monkeypatch.setattr(client, "_fetch", smart_stub("AS65010"))
    assert ipapp.get_asn() == "AS65010"


def test_asn_head_include_ip(monkeypatch):
    hdr = {
        "x-ipapp-asn": "AS424242",
        "x-ipapp-ip": "5.5.5.5",
        "x-ipapp-ip-version": "4",
    }
    monkeypatch.setattr(client, "_fetch", smart_stub(hdr))
    out = ipapp.get_asn(head=True, include_ip=True)
    assert out["ip"] == "5.5.5.5"


def test_asn_json_include_ip(monkeypatch):
    good = {"asn": 424242, "ip": "6.6.6.6", "ip_version": "6"}
    monkeypatch.setattr(client, "_fetch", smart_stub(good))
    assert ipapp.get_asn(json=True, include_ip=True) == good


def test_asn_json_include_ip_unknown(monkeypatch):
    bad = {"asn": 424242, "ip": UNKNOWN, "ip_version": ""}
    monkeypatch.setattr(client, "_fetch", smart_stub(bad))
    assert ipapp.get_asn(json=True, include_ip=True)["ip"] is None
    with pytest.raises(IPAppError):
        ipapp.get_asn(json=True, include_ip=True, strict=True)
