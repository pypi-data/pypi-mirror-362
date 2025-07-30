"""End-to-end tests for the ApiClient class."""

import unittest
from io import BytesIO
from multistamper.core.apiclient import ApiClient, StampData


class TestApiClientE2E(unittest.TestCase):
    """
    TestApiClientE2E is an end-to-end test for the ApiClient.
    It tests the main functionalities of the ApiClient against a live API.
    """

    def setUp(self):
        self.client = ApiClient(
            "https://dev.app.vbase.com", "7QaH1ky0msl6PIVtGzqUWVDMj6mwl23Hui6N1H8-YqA"
        )

    def test_stamp_dataCid_only(self):
        data: StampData = {
            "dataCid": "0x8508e5471887670c4229daddfbf86cc41288d7bc4f47672b3cadbe68f9eee60c",
            "storeStampedFiles": True,
        }

        result = self.client.stamp(input_data=data)
        self.assertIn("commitment_receipt", result)
        print("STAMP RESPONSE:", result)

    def test_stamp_with_file(self):
        file_obj = BytesIO(b"mock test data")
        file_obj.name = "__init__.py"

        data: StampData = {"storeStampedFiles": True}

        result = self.client.stamp(input_data=data, input_files={"file": file_obj})
        self.assertIn("commitment_receipt", result)
        print("STAMP (file) RESPONSE:", result)

    def test_verify(self):
        object_hashes = [
            "0x8508e5471887670c4229daddfbf86cc41288d7bc4f47672b3cadbe68f9eee60c"
        ]
        result = self.client.verify(object_hashes)
        self.assertIn("stamp_list", result)
        print("VERIFY RESPONSE:", result)

    def test_fetch_collections(self):
        result = self.client.fetch_collections()
        self.assertIsInstance(result, dict)
        self.assertIn("usercollections", result)
        print("COLLECTIONS:", result)

    def test_fetch_user_profile(self):
        result = self.client.fetch_user_profile()
        self.assertIn("email", result)
        self.assertEqual(result["name"], "romeokholoniuk12")
        print("USER PROFILE:", result)


if __name__ == "__main__":
    unittest.main()
