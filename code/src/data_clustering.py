import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Load the datasets
df_customers = pd.read_csv("customer_data.csv")
df_financial_behavior = pd.read_csv("financial_behavior_data.csv")
df_enquiries = pd.read_csv("enquiries_data.csv")

# Debugging: Check column names before merging
print("📌 Columns in financial_behavior_data.csv:", df_financial_behavior.columns.tolist())
print("📌 Columns in enquiries_data.csv:", df_enquiries.columns.tolist())

# Merge datasets on Customer_ID
df_combined = df_customers.merge(df_financial_behavior, on="Customer_ID", how="left")
df_combined = df_combined.merge(df_enquiries, on="Customer_ID", how="left")

# Debugging: Check column names after merging
print("📌 Columns after merging:", df_combined.columns.tolist())

# Resolve 'Product_Type' column issue
if "Product_Type_x" in df_combined.columns and "Product_Type_y" in df_combined.columns:
    df_combined["Product_Type"] = df_combined["Product_Type_x"].fillna(df_combined["Product_Type_y"])
    df_combined.drop(["Product_Type_x", "Product_Type_y"], axis=1, inplace=True)
elif "Product_Type_x" in df_combined.columns:
    df_combined.rename(columns={"Product_Type_x": "Product_Type"}, inplace=True)
elif "Product_Type_y" in df_combined.columns:
    df_combined.rename(columns={"Product_Type_y": "Product_Type"}, inplace=True)
elif "Product_Type" not in df_combined.columns:
    raise ValueError("❌ 'Product_Type' column is missing after merging!")

# Drop non-numeric columns (except categorical ones used in clustering)
df_combined.drop(["Name", "Enquiry_Date"], axis=1, inplace=True)

# Define categorical & numerical features
categorical_cols = ["Spending_Habit", "Risk_Profile", "Engagement_Level", "Product_Type", "Default_Status", "Status"]
numerical_cols = [
    "Age", "Income", "Transactions", "Sentiment_Score", "Loan_Amount", 
    "Credit_Limit", "Credit_Utilization", "EMI_Paid", "Tenure_Months", 
    "Max_DPD", "Enquiry_Amount"
]

# Fill missing values for numerical and categorical features
df_combined[numerical_cols] = df_combined[numerical_cols].fillna(df_combined[numerical_cols].median())
df_combined[categorical_cols] = df_combined[categorical_cols].fillna(df_combined[categorical_cols].mode().iloc[0])

# Preprocessing: Scale numerical features & One-Hot Encode categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),  
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

# K-Means clustering pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("kmeans", KMeans(n_clusters=5, random_state=42, n_init=10))  # 5 customer segments
])

# Fit & predict clusters
df_combined["Cluster"] = pipeline.fit_predict(df_combined)

# Save clustered data
df_combined.to_csv("clustered_customer_data.csv", index=False)
print("✅ Customer clustering completed! Data saved as clustered_customer_data.csv")
