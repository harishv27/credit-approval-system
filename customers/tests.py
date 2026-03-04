from django.test import TestCase
from customers.models import Customer

class CustomerTest(TestCase):

    def test_customer_creation(self):

        customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            age=25,
            phone_number="9999999999",
            monthly_salary=50000,
            approved_limit=1800000
        )

        self.assertEqual(customer.first_name, "Test")