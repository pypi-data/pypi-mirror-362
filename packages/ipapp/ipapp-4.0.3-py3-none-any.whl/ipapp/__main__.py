"""CLI entry-point: `python -m ipapp` or `ipapp`."""

from __future__ import annotations

import argparse
import sys
from typing import Any, Callable

from . import get_asn, get_location, get_ip, get_tz


def _printer(func: Callable[..., Any], *args, **kwargs) -> None:
    res = func(*args, **kwargs)
    print(res if isinstance(res, str) else _pretty(res))


def _pretty(obj: Any) -> str:
    if not isinstance(obj, dict):
        return str(obj)
    return "{" + ", ".join(f"{k}={v!r}" for k, v in obj.items()) + "}"


def main(argv: list[str] | None = None) -> None:  # noqa: D401
    parser = argparse.ArgumentParser(prog="ipapp", description="Query ip.app")
    sub = parser.add_subparsers(dest="cmd")

    # ip
    p_ip = sub.add_parser("ip")
    p_ip.add_argument("--json", action="store_true")
    p_ip.add_argument("--head", action="store_true")
    p_ip.add_argument("--strict", action="store_true")

    # asn
    p_asn = sub.add_parser("asn")
    p_asn.add_argument("--json", action="store_true")
    p_asn.add_argument("--head", action="store_true")
    p_asn.add_argument("--include-ip", action="store_true")
    p_asn.add_argument("--strict", action="store_true")

    # location
    p_location = sub.add_parser("location")
    p_location.add_argument("--json", action="store_true", default=False)
    p_location.add_argument("--head", action="store_true")
    p_location.add_argument("--include-ip", action="store_true")
    p_location.add_argument("--strict", action="store_true")

    # tz
    p_tz = sub.add_parser("tz")
    p_tz.add_argument("--head", action="store_true")
    p_tz.add_argument("--json", action="store_true")
    p_tz.add_argument("--include-ip", action="store_true")
    p_tz.add_argument("--strict", action="store_true")

    args = parser.parse_args(args=argv)

    match args.cmd:
        case "ip" | None:
            _printer(
                get_ip,
                json=args.json,
                head=args.head,
                strict=args.strict,
            )
        case "tz":
            _printer(
                get_tz,
                head=args.head,
                include_ip=args.include_ip,
                json=args.json,
                strict=args.strict,
            )
        case "location":
            # if --head was given, ignore any --json flag
            _printer(
                get_location,
                json=(args.json and not args.head),
                head=args.head,
                include_ip=args.include_ip,
                strict=args.strict,
            )
        case "asn":
            _printer(
                get_asn,
                json=args.json,
                head=args.head,
                include_ip=args.include_ip,
                strict=args.strict,
            )


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
