import unittest

from erc7730_deployment_check import check


class DeploymentCheckTests(unittest.TestCase):
    def test_accepts_well_formed_binding(self):
        messages, valid = check({"context": {"contract": {"deployments": [{"chainId": 1, "address": "0x1111111111111111111111111111111111111111"}]}}})
        self.assertTrue(valid)
        self.assertIn("Found 1 well-formed", messages[0])

    def test_rejects_non_object_descriptor_in_public_function(self):
        for descriptor in (None, [], "descriptor", 1):
            with self.subTest(descriptor=descriptor):
                messages, valid = check(descriptor)
                self.assertFalse(valid)
                self.assertEqual(messages, ["descriptor root must be a JSON object."])

    def test_rejects_duplicate_chain_address_binding(self):
        deployment = {"chainId": 1, "address": "0x1111111111111111111111111111111111111111"}
        messages, valid = check({"context": {"contract": {"deployments": [deployment, deployment]}}})
        self.assertFalse(valid)
        self.assertTrue(any("duplicates a chain and address" in message for message in messages))

    def test_rejects_boolean_chain_id(self):
        messages, valid = check({"context": {"contract": {"deployments": [{"chainId": True, "address": "0x1111111111111111111111111111111111111111"}]}}})
        self.assertFalse(valid)
        self.assertTrue(any("positive uint256 integer" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
