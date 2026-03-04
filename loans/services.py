from customers.models import Customer
from loans.models import Loan
from core.utils import calculate_credit_score, calculate_emi


def check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure):

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return None, "Customer not found"

    credit_score = calculate_credit_score(customer)

    loans = Loan.objects.filter(customer=customer)

    total_emi = sum(loan.monthly_repayment for loan in loans)

    if total_emi > 0.5 * customer.monthly_salary:
        return None, "EMI exceeds allowed limit"

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
        return None, "Loan not approved"

    emi = calculate_emi(loan_amount, corrected_interest, tenure)

    return {
        "customer": customer,
        "emi": emi,
        "interest_rate": corrected_interest
    }, None