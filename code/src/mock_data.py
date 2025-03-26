import pandas as pd
import random
from faker import Faker

fake = Faker()

# Number of customers
num_customers = 100
customer_ids = list(range(1, num_customers + 1))

# Possible categories
spending_habits = ["Luxury", "Budget", "Premium", "Moderate"]
risk_profiles = ["Low", "Moderate", "High"]
engagement_levels = ["High", "Medium", "Low"]
product_types = ["Credit Card", "Personal Loan", "Mortgage", "Auto Loan", "Investment Account"]

# Generate customer data
customers = []
financial_behaviors = []
enquiries = []

for i in customer_ids:
    # Base customer data
    customer = {
        "Customer_ID": i,
        "Name": f"Customer_{i}",
        "Age": random.randint(20, 70),
        "Income": random.randint(30000, 120000),
        "Spending_Habit": random.choice(spending_habits),
        "Risk_Profile": random.choice(risk_profiles),
        "Transactions": random.randint(1, 50),
        "Sentiment_Score": round(random.uniform(-1, 1), 2),  # Range: -1 to 1
        "Engagement_Level": random.choice(engagement_levels),
    }
    customers.append(customer)

    # Financial behavior data
    product_type = random.choice(product_types)
    loan_amount = random.randint(5000, 50000) if product_type != "Investment Account" else 0
    credit_limit = random.randint(1000, 20000)
    utilization = round(random.uniform(0.1, 0.9), 2)  # Credit utilization (10% - 90%)
    max_dpd = random.randint(0, 90)  # Max days past due
    default_status = random.choice(["No Default", "Minor Delay", "Major Default"])
    
    financial_behavior = {
        "Customer_ID": i,
        "Product_Type": product_type,
        "Loan_Amount": loan_amount,
        "Credit_Limit": credit_limit,
        "Credit_Utilization": utilization,
        "EMI_Paid": random.randint(1, 24),
        "Tenure_Months": random.randint(12, 60),
        "Max_DPD": max_dpd,
        "Default_Status": default_status,
    }
    financial_behaviors.append(financial_behavior)

    # Enquiry data
    enquiry = {
        "Customer_ID": i,
        "Enquiry_Date": fake.date_between(start_date='-90d', end_date='today'),
        "Product_Type": product_type,
        "Enquiry_Amount": random.randint(5000, 100000),
        "Status": random.choice(["Approved", "Rejected"]),
    }
    enquiries.append(enquiry)

# Convert to DataFrames
df_customers = pd.DataFrame(customers)
df_financial_behavior = pd.DataFrame(financial_behaviors)
df_enquiries = pd.DataFrame(enquiries)

# Save to CSV
df_customers.to_csv("customer_data.csv", index=False)
df_financial_behavior.to_csv("financial_behavior_data.csv", index=False)
df_enquiries.to_csv("enquiries_data.csv", index=False)

print("Mock customer data, financial behavior data, and enquiries data generated successfully!")