from rest_framework import serializers
from .models import Customer

class CustomerRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "monthly_salary",
            "approved_limit"
        ]

        read_only_fields = ["customer_id", "approved_limit"]