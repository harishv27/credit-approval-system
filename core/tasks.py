from celery import shared_task
import pandas as pd

from customers.models import Customer



@shared_task
def load_customer_data():

    df = pd.read_excel("data/customer_data.xlsx")

    print("Total customers:", len(df))

    for _, row in df.iterrows():

        Customer.objects.update_or_create(
            customer_id=row["Customer ID"],
            defaults={
                "first_name": row["First Name"],
                "last_name": row["Last Name"],
                "age": row["Age"],
                "phone_number": str(row["Phone Number"]),
                "monthly_salary": row["Monthly Salary"],
                "approved_limit": row["Approved Limit"],
                "current_debt": 0
            }
        )



from loans.models import Loan
from customers.models import Customer
from datetime import datetime

@shared_task
def load_loan_data():

    df = pd.read_excel("data/loan_data.xlsx")

    print("Total loans:", len(df))

    for _, row in df.iterrows():

        try:
            customer = Customer.objects.get(customer_id=row["Customer ID"])
        except Customer.DoesNotExist:
            print("Customer missing:", row["Customer ID"])
            continue

        Loan.objects.update_or_create(
            loan_id=row["Loan ID"],
            defaults={
                "customer": customer,
                "loan_amount": row["Loan Amount"],
                "tenure": row["Tenure"],
                "interest_rate": row["Interest Rate"],
                "monthly_repayment": row["Monthly payment"],
                "emis_paid_on_time": row["EMIs paid on Time"],
                "start_date": row["Date of Approval"],
                "end_date": row["End Date"]
            }
        )