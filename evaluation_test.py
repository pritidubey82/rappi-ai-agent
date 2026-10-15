# evaluation_test.py
import sys
import os
import unittest

# Dynamic import path adjustment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.validator import validate_and_execute_recommendation
from app.database import MOCK_DB

class TestPurchasingAgentValidation(unittest.TestCase):

    def setUp(self):
        MOCK_DB["inventory"]["SKU-101"]["current_stock"] = 150
        MOCK_DB["budget"]["available"] = 2000.00
        MOCK_DB["purchase_orders"] = []

    def test_scenario_1_over_storage_capacity(self):
        result = validate_and_execute_recommendation("SKU-101", "SUPP-01", 800)
        self.assertEqual(result["status"], "MODIFIED")
        self.assertEqual(result["executed_quantity"], 350)
        self.assertIn("purchase_order", result)
        self.assertEqual(result["purchase_order"]["quantity"], 350)

    def test_scenario_acceptable_order(self):
        result = validate_and_execute_recommendation("SKU-101", "SUPP-01", 200)
        self.assertEqual(result["status"], "ACCEPTED")
        self.assertEqual(result["executed_quantity"], 200)

    def test_scenario_below_moq_rejection(self):
        result = validate_and_execute_recommendation("SKU-101", "SUPP-01", 50)
        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(result["executed_quantity"], 0)

if __name__ == "__main__":
    unittest.main()