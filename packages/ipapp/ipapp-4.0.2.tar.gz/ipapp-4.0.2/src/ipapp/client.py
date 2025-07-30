"""
ipapp HTTP helpers + public API wrappers.

Each endpoint supports three modes:

  • Plain text (default)
  • JSON body        json=True
  • Header-only      head=True

For non-root endpoints you may also request that the caller's IP be
injected into the JSON result:

    ipapp.get_asn(json=True, include_ip=True)
"""

from __future__ import annotations

import json as _json
from typing import Any
from urllib import request as _req
from urllib.error import HTTPError, URLError

# constants (existing ones in your file)
_BASE_URL = "https://ip.app"
_TIMEOUT = 5
_IP_HDR = "x-ipapp-ip"
_IP_VER_HDR = "x-ipapp-ip-version"
_TZ_HDR = "x-ipapp-tz"
_ASN_HDR = "x-ipapp-asn"
UNKNOWN = "unknown"


class IPAppError(RuntimeError):
    """Raised when ip.app cannot be reached or returns invalid data."""


def _convert_numeric_booleans(data: Any) -> Any:
    """Convert numeric boolean fields to proper booleans."""
    if isinstance(data, dict):
        result = data.copy()
        if "is_eu_country" in result:
            if isinstance(result["is_eu_country"], (int, str)):
                result["is_eu_country"] = bool(int(result["is_eu_country"]))
        return result
    return data


def _fetch(
    path: str,
    *,
    json: bool = False,          # noqa: A002
    head: bool = False,
    header: str | None = None,
    include_ip: bool = False,
    strict: bool = False,
) -> Any:
    """
    Core helper used by all public wrappers.

    Parameters
    ----------
    path        : route starting with '/', e.g. '/asn'
    json        : append '?format=json' and JSON-decode body
    head        : send HEAD instead of GET and read only headers
    header      : if *head* return just this header's value
    include_ip  : when GET+JSON, merge x-ipapp-ip(+version) headers
    strict      : raise `IPAppError` when the IP value is missing/Unknown

    Notes
    -----
    * exactly **one** of *json* or *head* may be True
    * *include_ip* is allowed with json=True **or** head=True
    """
    if head and json:
        raise ValueError("Choose either json=True or head=True, not both.")
    if include_ip and not (json or head):
        raise ValueError("include_ip requires json=True or head=True")

    url = f"{_BASE_URL}{path}"
    if json:
        url += ("&" if "?" in path else "?") + "format=json"

    req = _req.Request(url, method="HEAD" if head else "GET")

    try:
        with _req.urlopen(req, timeout=_TIMEOUT) as resp:
            # HEAD branch
            if head:
                if header is None:
                    hdrs: dict[str, str] = dict(resp.headers)
                    if include_ip:
                        ip_val = hdrs.get(_IP_HDR)
                        ip_ver = hdrs.get(_IP_VER_HDR)
                        if ip_val is not None:
                            hdrs["ip"] = (
                                None
                                if ip_val.lower() == "unknown"
                                else ip_val
                            )
                            hdrs["ip_version"] = (
                                None
                                if ip_ver is None or ip_ver.lower() == "unknown"
                                else ip_ver
                            )
                        elif strict:
                            raise IPAppError("IP address unknown")
                    return _convert_numeric_booleans(hdrs)

                val = resp.headers.get(header)
                if header.lower() == _IP_HDR:
                    if val is None or val.lower() == UNKNOWN:
                        if strict:
                            raise IPAppError("IP address unknown")
                        return None
                return val.strip() if val is not None else None

            # GET branch
            body = resp.read()
            ip_val: str | None = None
            ip_ver: str | None = None
            if include_ip:
                ip_val = resp.headers.get(_IP_HDR)
                ip_ver = resp.headers.get(_IP_VER_HDR)
                if strict and (
                    ip_val is None or ip_val.lower() == UNKNOWN
                ):
                    raise IPAppError("IP address unknown")
    except (HTTPError, URLError) as exc:
        raise IPAppError(str(exc)) from exc

    # JSON body
    if json:
        try:
            data = _json.loads(body.decode())
        except _json.JSONDecodeError as exc:
            raise IPAppError("Invalid JSON") from exc

        # universal Unknown → None / raise
        if "ip" in data and isinstance(data["ip"], str):
            if data["ip"].lower() == UNKNOWN:
                if strict:
                    raise IPAppError("IP address unknown")
                data["ip"] = None
        
        # convert numeric boolean fields to proper booleans
        data = _convert_numeric_booleans(data)

        if include_ip:
            data["ip"] = (
                None
                if ip_val is None or ip_val.lower() == UNKNOWN
                else ip_val
            )
            data["ip_version"] = (
                None
                if ip_ver is None or ip_ver.lower() in (UNKNOWN, "")
                else ip_ver
            )
        return data

    # plain-text body
    text = body.decode().strip()
    if text.lower() == UNKNOWN:
        if strict:
            raise IPAppError("IP address unknown")
        return None
    return text


# ---------------------------------------------------------------------------
# Public wrappers
# ---------------------------------------------------------------------------


def get_ip(
    *,
    json: bool = False,
    head: bool = False,
    strict: bool = False,
):  # noqa: A002
    """
    Return the caller's public IP address.

    ── Modes ──────────────────────────────────────────────────────────────
    • Plain text          -> "203.0.113.42" / None / raise
    • JSON (json=True)    -> {"ip": "..."}   / {"ip": None}
    • Header (head=True)  -> value of X-Ipapp-Ip header

    *strict*:
        Raise IPAppError instead of returning None when the
        service responds with "Unknown".
    """
    # Returns the IP address in header-only mode
    if head:
        return _fetch(
            "/",
            head=True,
            header=_IP_HDR,
            include_ip=False,
            strict=strict,
        )

    # Returns the IP address in JSON mode
    if json:
        data = _fetch(
            "/",
            json=True,
            include_ip=False,
            strict=strict,
        )
        if data.get("ip") == "Unknown":
            if strict:
                raise IPAppError("IP address unknown")
            data["ip"] = None
        return data

    # Returns the IP address in plain-text mode
    # Explicitly exclude caller IP to avoid duplication with the IP address string
    return _fetch(
        "/",
        include_ip=False,
        strict=strict,
    )

def get_tz(
    *,
    json: bool = False,
    head: bool = False,
    include_ip: bool = False,
    strict: bool = False,
):  # noqa: A002
    """Return timezone string (or dict in JSON mode).

    The returned value is the timezone string as reported by ip.app.

    Modes
    -----
    • JSON body  (default)          -> dict from response body
    • HEAD-only  (head=True)        -> dict built from X-Ipapp-* response lines
    • Plain text (json=False)       -> raw plain-text dump

    *include_ip*   merges caller IP into the JSON body.
    *strict*       raises IPAppError if the caller IP is “Unknown”.
    """
    # Returns the timezone string in header-only mode with or without caller IP
    if head:
        if include_ip:
            hdr = _fetch("/tz", head=True, header=None, strict=strict)
            tz  = hdr.get(_TZ_HDR)
            ip  = hdr.get(_IP_HDR)
            ver = hdr.get(_IP_VER_HDR)
            if strict and (ip in (None, "Unknown")):
                raise IPAppError("IP address unknown")
            # Returns the timezone string in header-only mode with caller IP
            response = {
                "tz": tz,
                "ip": None if ip in (None, "Unknown") else ip,
                "ip_version": None if ver in (None, "Unknown") else ver,
            }
            # Add any additional headers that might contain boolean fields
            for key, value in hdr.items():
                if key.lower() not in [_TZ_HDR, _IP_HDR, _IP_VER_HDR]:
                    response[key] = value
            return _convert_numeric_booleans(response)
        # Returns the timezone string in header-only mode without caller IP
        return _fetch(
            "/tz",
            head=True,
            header=_TZ_HDR,
            strict=strict,
        )
    # Returns the timezone string in JSON mode with or without caller IP
    if json:
        return _fetch(
            "/tz",
            json=True,
            include_ip=include_ip,
            strict=strict,
        )
    # Returns the timezone string in plain-text mode without caller IP
    # Explicitly exclude caller IP to avoid confusion with the timezone string
    return _fetch(
        "/tz",
        include_ip=False,
        strict=strict,
    )

def get_location(
    *,
    json: bool = True,
    head: bool = False,
    include_ip: bool = False,
    strict: bool = False,
):  # noqa: A002
    """
    Return the request location seen by ip.app.

    Modes
    -----
    • JSON body  (default)          -> dict from response body
    • HEAD-only  (head=True)        -> dict built from x-ipapp-* response lines
    • Plain text (json=False)       -> raw plain-text dump

    *include_ip*   merges caller IP into the JSON body.
    *strict*       raises IPAppError if the caller IP is “Unknown”.
    """
    # Returns the location in header-only mode with or without caller IP
    if head:
        # grab the **entire** header map and filter down below
        hdrs = _fetch(
            "/loc",
            head=True,
            header=None,
            include_ip=include_ip,
            strict=strict,
        )

        prefixes = [
            "x-ipapp-loc-",
        ]
        # if include_ip is True, add the IP and IP version headers
        if include_ip:
            prefixes.append('x-ipapp-')

        result: dict[str, str] = {}

        for key, value in hdrs.items():
            lk = key.lower()
            for p in prefixes:
                if lk.startswith(p):
                    clean = lk[len(p) :]        # drop the prefix
                    result[clean] = value
                    break

        if strict and not result:
            raise IPAppError("no x-ipapp-* request headers found")
        return _convert_numeric_booleans(result)

    # Returns the location in JSON mode with or without caller IP
    if json:
        return _fetch(
            "/loc",
            json=True,
                include_ip=include_ip,
                strict=strict,
            )
    # Returns the location in plain-text mode without caller IP
    # Explicitly exclude caller IP to avoid confusion with the location string
    return _fetch(
        "/loc",
        include_ip=False,
        strict=strict,
    )


def get_asn(
    *,
    json: bool = False,
    head: bool = False,
    include_ip: bool = False,
    strict: bool = False,
):  # noqa: A002
    """Return ASN string, JSON dict, or header-only value.

    Modes
    -----
    • JSON body  (default)          -> dict from response body
    • HEAD-only  (head=True)        -> dict built from X-Ipapp-* response lines
    • Plain text (json=False)       -> raw plain-text dump

    *include_ip*   merges caller IP into the JSON body.
    *strict*       raises IPAppError if the caller IP is “Unknown”.
    """
    # Returns the ASN string in header-only mode with or without caller IP
    if head:
        if include_ip:
            hdr = _fetch("/asn", head=True, header=None, strict=strict)
            asn = hdr.get(_ASN_HDR)
            ip  = hdr.get(_IP_HDR)
            ver = hdr.get(_IP_VER_HDR)
            if strict and (ip in (None, "Unknown")):
                raise IPAppError("IP address unknown")
            # Returns the ASN string in header-only mode with caller IP
            response = {
                "asn": asn,
                "ip": None if ip in (None, "Unknown") else ip,
                "ip_version": None if ver in (None, "Unknown") else ver,
            }
            # Add any additional headers that might contain boolean fields
            for key, value in hdr.items():
                if key.lower() not in [_ASN_HDR, _IP_HDR, _IP_VER_HDR]:
                    response[key] = value
            return _convert_numeric_booleans(response)
        # Returns the ASN string in header-only mode without caller IP
        return _fetch(
            "/asn",
            head=True,
            header=_ASN_HDR,
            strict=strict,
        )

    # Returns the ASN string in JSON mode with or without caller IP
    if json:
        return _fetch(
            "/asn",
            json=True,
            include_ip=include_ip,
            strict=strict,
        )
    # Returns the ASN string in plain-text mode without caller IP
    # Explicitly exclude caller IP to avoid confusion with the ASN string
    return _fetch(
        "/asn",
        include_ip=False,
        strict=strict,
    )
