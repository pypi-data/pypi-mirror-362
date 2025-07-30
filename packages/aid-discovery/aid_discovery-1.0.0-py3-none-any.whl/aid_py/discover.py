# MIT License
# Copyright (c) 2025 Agent Community
# Author: Agent Community
# Repository: https://github.com/agentcommunity/agent-interface-discovery
"""DNS discovery client for Agent Interface Discovery (AID).

Uses `dnspython` to query the `_agent.<domain>` TXT record, validates it
with `aid_py.parse`, and returns the parsed record together with the DNS TTL.
"""
from __future__ import annotations

from typing import Tuple

import dns.exception
import dns.resolver

from .constants import DNS_SUBDOMAIN
from .parser import AidError, parse

__all__ = ["discover"]


def _query_txt_record(fqdn: str, timeout: float) -> Tuple[list[str], int]:
    """Return list of TXT strings and TTL or raise AidError on DNS failure."""

    try:
        answers = dns.resolver.resolve(fqdn, "TXT", lifetime=timeout)
    except dns.resolver.NXDOMAIN as exc:
        raise AidError("ERR_NO_RECORD", str(exc)) from None
    except (dns.resolver.Timeout, dns.exception.DNSException) as exc:
        raise AidError("ERR_DNS_LOOKUP_FAILED", str(exc)) from None

    # dnspython joins multi-string automatically? Actually each answer.rdata.strings
    ttl = answers.rrset.ttl if answers.rrset else DNS_TTL_DEFAULT
    txt_strings: list[str] = []
    for rdata in answers:
        # each rdata.strings is a tuple of bytes segments
        txt_strings.append("".join(seg.decode() for seg in rdata.strings))
    return txt_strings, ttl


DNS_TTL_DEFAULT = 300  # fallback


def discover(domain: str, *, protocol: str | None = None, timeout: float = 5.0) -> Tuple[dict, int]:
    """Discover and validate the AID record for *domain*.

    Can optionally try a protocol-specific subdomain first.

    Returns a tuple `(record_dict, ttl_seconds)`.
    Raises `AidError` on any failure as per the specification.
    """

    # IDN → A-label conversion per RFC5890
    try:
        import idna

        domain_alabel = idna.encode(domain).decode()
    except Exception:
        domain_alabel = domain  # Fallback – let DNS resolver handle errors

    def _query_and_parse(query_name: str) -> Tuple[dict, int]:
        """Query a specific FQDN and parse the result."""
        txt_records, ttl = _query_txt_record(query_name, timeout)

        last_error: AidError | None = None
        for txt in txt_records:
            try:
                record = parse(txt)
                return record, ttl
            except AidError as exc:
                # Save and try the next TXT string (if multiple records exist)
                last_error = exc
                continue

        # If we got here, either no records or all invalid
        if last_error is not None:
            raise last_error
        raise AidError("ERR_NO_RECORD", f"No valid _agent TXT record found for {query_name}")

    # Try protocol-specific subdomain first if specified
    if protocol:
        protocol_fqdn = f"{DNS_SUBDOMAIN}.{protocol}.{domain_alabel}".rstrip(".")
        try:
            return _query_and_parse(protocol_fqdn)
        except AidError as exc:
            if exc.error_code != "ERR_NO_RECORD":
                raise exc
            # else: fall through to base domain query

    # Fallback or default: query the base _agent subdomain
    base_fqdn = f"{DNS_SUBDOMAIN}.{domain_alabel}".rstrip(".")
    return _query_and_parse(base_fqdn) 