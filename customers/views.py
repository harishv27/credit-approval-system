from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Customer
from .serializers import CustomerRegisterSerializer
from core.utils import calculate_approved_limit


@api_view(["POST"])
def register_customer(request):

    data = request.data

    approved_limit = calculate_approved_limit(data["monthly_income"])

    customer = Customer.objects.create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        phone_number=data["phone_number"],
        monthly_salary=data["monthly_income"],
        approved_limit=approved_limit,
        current_debt=0
    )

    serializer = CustomerRegisterSerializer(customer)

    return Response(serializer.data, status=status.HTTP_201_CREATED)