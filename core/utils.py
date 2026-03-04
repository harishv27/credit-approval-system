import math
from loans.models import Loan
from datetime import datetime


# APPROVED LIMIT CALCULATION
def calculate_approved_limit(monthly_salary):

    limit = 36 * monthly_salary

    lakh = 100000
    rounded_limit = round(limit / lakh) * lakh

    return rounded_limit


# EMI CALCULATION
def calculate_emi(principal, annual_interest_rate, tenure):

    monthly_rate = annual_interest_rate / (12 * 100)

    emi = (
        principal
        * monthly_rate
        * pow(1 + monthly_rate, tenure)
        / (pow(1 + monthly_rate, tenure) - 1)
    )

    return round(emi, 2)


# CREDIT SCORE CALCULATION
def calculate_credit_score(customer):

    loans = Loan.objects.filter(customer=customer)

    if not loans.exists():
        return 50

    score = 0

    total_loans = loans.count()

    on_time = sum([loan.emis_paid_on_time for loan in loans])

    if on_time > 0:
        score += 40

    if total_loans > 2:
        score += 20

    current_year = datetime.now().year

    recent_loans = loans.filter(start_date__year=current_year)

    if recent_loans.exists():
        score += 20

    total_amount = sum([loan.loan_amount for loan in loans])

    if total_amount < customer.approved_limit:
        score += 20

    return min(score, 100)