from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from customers.models import Customer
from loans.models import Loan
from core.utils import calculate_emi, calculate_credit_score


# -----------------------------
# CHECK LOAN ELIGIBILITY
# -----------------------------
@api_view(["POST"])
def check_eligibility(request):

    customer_id = request.data.get("customer_id")
    loan_amount = request.data.get("loan_amount")
    interest_rate = request.data.get("interest_rate")
    tenure = request.data.get("tenure")

    # Validate request data
    if not all([customer_id, loan_amount, interest_rate, tenure]):
        return Response(
            {"error": "Missing required fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {"error": "Customer not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    loan_amount = float(loan_amount)
    interest_rate = float(interest_rate)
    tenure = int(tenure)

    credit_score = calculate_credit_score(customer)

    # Check EMI rule
    loans = Loan.objects.filter(customer=customer)
    total_current_emi = sum(loan.monthly_repayment for loan in loans)

    if total_current_emi > (0.5 * customer.monthly_salary):
        return Response({
            "customer_id": customer_id,
            "approval": False,
            "message": "Total EMI exceeds 50% of monthly salary"
        })

    approval = False
    corrected_interest = interest_rate

    if credit_score > 50:
        approval = True

    elif 30 < credit_score <= 50:
        corrected_interest = max(interest_rate, 12)
        approval = interest_rate >= 12

    elif 10 < credit_score <= 30:
        corrected_interest = max(interest_rate, 16)
        approval = interest_rate >= 16

    else:
        approval = False

    emi = calculate_emi(loan_amount, corrected_interest, tenure)

    return Response({
        "customer_id": customer_id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_interest,
        "tenure": tenure,
        "monthly_installment": emi
    })


# -----------------------------
# CREATE LOAN
# -----------------------------
@api_view(["POST"])
def create_loan(request):

    customer_id = request.data.get("customer_id")
    loan_amount = request.data.get("loan_amount")
    interest_rate = request.data.get("interest_rate")
    tenure = request.data.get("tenure")

    if not all([customer_id, loan_amount, interest_rate, tenure]):
        return Response(
            {"error": "Missing required fields"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {"error": "Customer not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    loan_amount = float(loan_amount)
    interest_rate = float(interest_rate)
    tenure = int(tenure)

    credit_score = calculate_credit_score(customer)

    approval = False
    corrected_interest = interest_rate

    if credit_score > 50:
        approval = True

    elif 30 < credit_score <= 50:
        corrected_interest = max(interest_rate, 12)
        approval = interest_rate >= 12

    elif 10 < credit_score <= 30:
        corrected_interest = max(interest_rate, 16)
        approval = interest_rate >= 16

    if not approval:
        return Response({
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": "Loan not approved",
            "monthly_installment": None
        })

    emi = calculate_emi(loan_amount, corrected_interest, tenure)

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        tenure=tenure,
        interest_rate=corrected_interest,
        monthly_repayment=emi,
        emis_paid_on_time=0,
        start_date=date.today(),
        end_date=date.today()
    )

    return Response({
        "loan_id": loan.loan_id,
        "customer_id": customer_id,
        "loan_approved": True,
        "message": "Loan approved",
        "monthly_installment": emi
    })


# -----------------------------
# VIEW SINGLE LOAN
# -----------------------------
@api_view(["GET"])
def view_loan(request, loan_id):

    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response(
            {"error": "Loan not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    customer = loan.customer

    data = {
        "loan_id": loan.loan_id,
        "customer": {
            "id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age
        },
        "loan_amount": loan.loan_amount,
        "interest_rate": loan.interest_rate,
        "monthly_installment": loan.monthly_repayment,
        "tenure": loan.tenure
    }

    return Response(data)


# -----------------------------
# VIEW CUSTOMER LOANS
# -----------------------------
@api_view(["GET"])
def view_customer_loans(request, customer_id):

    loans = Loan.objects.filter(customer__customer_id=customer_id)

    if not loans.exists():
        return Response(
            {"message": "No loans found for this customer"},
            status=status.HTTP_404_NOT_FOUND
        )

    loan_list = []

    for loan in loans:

        repayments_left = loan.tenure - loan.emis_paid_on_time

        loan_list.append({
            "loan_id": loan.loan_id,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "repayments_left": repayments_left
        })

    return Response(loan_list)