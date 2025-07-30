# aid-discovery (Python)

> Official Python implementation of the [Agent Interface Discovery (AID)](https://github.com/agentcommunity/agent-interface-discovery) specification.

[![PyPI version](https://img.shields.io/pypi/v/aid-discovery.svg?color=blue)](https://pypi.org/project/aid-discovery/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

AID enables you to discover AI agents by domain name using DNS TXT records. Type a domain, get the agent's endpoint and protocol - that's it.

## Installation

```bash
pip install aid-discovery
```

## Quick Start

```python
from aid_py import discover, AidError

try:
    # Discover an agent by domain
    result = discover("supabase.agentcommunity.org")

    print(f"Protocol: {result.record.proto}")  # "mcp"
    print(f"URI: {result.record.uri}")         # "https://api.supabase.com/mcp"
    print(f"Description: {result.record.desc}") # "Supabase MCP"
    print(f"TTL: {result.ttl} seconds")

except AidError as e:
    print(f"Discovery failed: {e}")
```

## API Reference

### `discover(domain: str) -> DiscoveryResult`

Discovers an agent by looking up the `_agent` TXT record for the given domain.

**Parameters:**

- `domain` (str): The domain name to discover

**Returns:**

- `DiscoveryResult`: Object containing the parsed record and TTL

**Raises:**

- `AidError`: If discovery fails for any reason

### `parse(txt: str) -> AidRecord`

Parses and validates a raw TXT record string.

**Parameters:**

- `txt` (str): Raw TXT record content (e.g., "v=aid1;uri=https://...")

**Returns:**

- `AidRecord`: Parsed and validated record

**Raises:**

- `AidError`: If parsing or validation fails

## Data Types

### `AidRecord`

Represents a parsed AID record with the following attributes:

- `v` (str): Protocol version (always "aid1")
- `uri` (str): Agent endpoint URI
- `proto` (str): Protocol identifier (e.g., "mcp", "openapi")
- `auth` (str, optional): Authentication method
- `desc` (str, optional): Human-readable description

### `DiscoveryResult`

Contains discovery results:

- `record` (AidRecord): The parsed AID record
- `ttl` (int): DNS TTL in seconds

### `AidError`

Exception raised when discovery or parsing fails:

- `code` (int): Numeric error code
- `message` (str): Human-readable error message

## Error Codes

| Code | Symbol                  | Description                  |
| ---- | ----------------------- | ---------------------------- |
| 1000 | `ERR_NO_RECORD`         | No `_agent` TXT record found |
| 1001 | `ERR_INVALID_TXT`       | Record found but malformed   |
| 1002 | `ERR_UNSUPPORTED_PROTO` | Protocol not supported       |
| 1003 | `ERR_SECURITY`          | Security policy violation    |
| 1004 | `ERR_DNS_LOOKUP_FAILED` | DNS query failed             |

## Advanced Usage

### Custom Error Handling

```python
from aid_py import discover, AidError

try:
    result = discover("example.com")
    # Use result.record...
except AidError as e:
    if e.code == 1000:  # ERR_NO_RECORD
        print("No agent found for this domain")
    elif e.code == 1001:  # ERR_INVALID_TXT
        print("Found a record but it's malformed")
    else:
        print(f"Other error: {e}")
```

### Parsing Raw Records

```python
from aid_py import parse, AidError

txt_record = "v=aid1;uri=https://api.example.com/agent;proto=mcp;desc=Example Agent"

try:
    record = parse(txt_record)
    print(f"Parsed: {record.proto} agent at {record.uri}")
except AidError as e:
    print(f"Invalid record: {e}")
```

## Development

This package is part of the [AID monorepo](https://github.com/agentcommunity/agent-interface-discovery). To run tests:

```bash
# From the monorepo root
pnpm test

# Or run Python tests directly
cd packages/aid-py
python -m pytest tests/
```

## License

MIT - see [LICENSE](https://github.com/agentcommunity/agent-interface-discovery/blob/main/LICENSE) for details.
