# ERC-7730 Deployment Check

A tiny Python command-line check for the EVM chain and address bindings in an ERC-7730 descriptor.

```powershell
python erc7730_deployment_check.py example.json
```

It catches missing or malformed deployment bindings and duplicate chain/address entries. It does not validate the complete ERC-7730 schema, descriptor attestations, deployed bytecode, or whether a transaction is safe. Treat its output as a basic input check, not an audit.

This is an AI-assisted draft. Review and change it before publishing it under your profile.
