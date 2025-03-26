import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the clustered dataset
df = pd.read_csv("clustered_customer_data.csv")

# Drop ID (not needed) and separate target
X = df.drop(["Customer_ID", "Cluster"], axis=1)
y = df["Cluster"]

# Identify categorical and numerical columns
categorical_cols = ["Spending_Habit", "Risk_Profile", "Engagement_Level", "Product_Type", "Default_Status", "Status"]
numerical_cols = [
    "Age", "Income", "Transactions", "Sentiment_Score", "Loan_Amount",
    "Credit_Limit", "Credit_Utilization", "EMI_Paid", "Tenure_Months",
    "Max_DPD", "Enquiry_Amount"
]

# Handle missing values (just in case)
X[categorical_cols] = X[categorical_cols].fillna(X[categorical_cols].mode().iloc[0])
X[numerical_cols] = X[numerical_cols].fillna(X[numerical_cols].median())

# Define preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

# Create full training pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Save the full pipeline (model + preprocessing)
joblib.dump(pipeline, "customer_clustering_model.pkl")
print("✅ Model training complete. Model saved as customer_clustering_model.pkl")
