# ERC-7730 Deployment Check

A tiny Python command-line check for the EVM chain and address bindings in an ERC-7730 descriptor.

```powershell
python erc7730_deployment_check.py example.json
```

It catches missing or malformed deployment bindings, chain IDs outside the positive uint256 range, and duplicate chain/address entries. Descriptor objects with duplicate keys are rejected to avoid silently choosing between conflicting values. It does not validate the complete ERC-7730 schema, descriptor attestations, deployed bytecode, or whether a transaction is safe. Treat its output as a basic input check, not an audit.

This is an AI-assisted draft. Review and change it before publishing it under your profile.
