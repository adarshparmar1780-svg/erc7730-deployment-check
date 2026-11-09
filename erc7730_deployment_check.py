"""Check the EVM deployment bindings in an ERC-7730 JSON descriptor."""

import json
import re
import sys
from pathlib import Path


ADDRESS = re.compile(r"0x[0-9a-fA-F]{40}\Z")
UINT256_MAX = (1 << 256) - 1


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def check(descriptor):
    if not isinstance(descriptor, dict):
        return ["descriptor root must be a JSON object."], False
    context = descriptor.get("context", {})
    if not isinstance(context, dict):
        return ["context must be a JSON object."], False
    contract = context.get("contract")
    if not isinstance(contract, dict):
        return ["No EVM contract context found; this checker did not inspect the descriptor."], False

    deployments = contract.get("deployments")
    if not isinstance(deployments, list) or not deployments:
        return ["No contract deployments found; chain and address binding is missing."], False

    messages = []
    seen = set()
    valid = True
    for index, deployment in enumerate(deployments):
        if not isinstance(deployment, dict):
            messages.append(f"deployments[{index}] must be an object.")
            valid = False
            continue

        chain_id = deployment.get("chainId")
        address = deployment.get("address")
        if isinstance(chain_id, bool) or not isinstance(chain_id, int) or not 0 < chain_id <= UINT256_MAX:
            messages.append(f"deployments[{index}].chainId must be a positive uint256 integer.")
            valid = False
        if not isinstance(address, str) or not ADDRESS.fullmatch(address):
            messages.append(f"deployments[{index}].address must be a 20-byte 0x-prefixed address.")
            valid = False
        if isinstance(chain_id, int) and not isinstance(chain_id, bool) and isinstance(address, str):
            key = (chain_id, address.lower())
            if key in seen:
                messages.append(f"deployments[{index}] duplicates a chain and address binding.")
                valid = False
            seen.add(key)

    if valid:
        messages.append(f"Found {len(deployments)} well-formed deployment binding(s).")
    return messages, valid


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} DESCRIPTOR.json", file=sys.stderr)
        return 2
    try:
        descriptor = json.loads(
            Path(sys.argv[1]).read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
        )
    except (OSError, ValueError) as error:
        print(f"Cannot read descriptor: {error}", file=sys.stderr)
        return 2
    if not isinstance(descriptor, dict):
        print("Descriptor root must be a JSON object.", file=sys.stderr)
        return 2

    messages, valid = check(descriptor)
    for message in messages:
        print(message)
    print("This check does not validate descriptor integrity or transaction safety.")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
