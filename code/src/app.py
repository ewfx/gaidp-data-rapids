from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from recommendation_engine import generate_recommendation

app = Flask(__name__)


CORS(app, origins=["http://localhost:3000"])

# Load the model and dataset
model = joblib.load("customer_clustering_model.pkl")
df = pd.read_csv("clustered_customer_data.csv")

# In-memory feedback store (dictionary with customer_id as key)
user_feedback_memory = {}

@app.route("/recommend", methods=["GET"])
def recommend():
    customer_id = request.args.get("customer_id")

    if not customer_id:
        return jsonify({"error": "Customer ID is required"}), 400

    customer_id = int(customer_id)
    customer_row = df[df["Customer_ID"] == customer_id]

    if customer_row.empty:
        return jsonify({"error": "Customer not found"}), 404

    input_features = customer_row.drop(["Customer_ID", "Cluster"], axis=1)
    cluster_id = model.predict(input_features)[0]

    feedback = user_feedback_memory.get(customer_id, [])
    personalized_recommendation = generate_recommendation(cluster_id, user_feedback=feedback)

    return jsonify({
        "customer_id": customer_id,
        "cluster_id": int(cluster_id),
        "feedback": feedback,
        "personalized_recommendation": personalized_recommendation
    })

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    customer_id = data.get("customer_id")
    feedback_items = data.get("feedback")  # List of feedback strings

    if customer_id is None or not isinstance(feedback_items, list):
        return jsonify({"error": "Invalid input format. Provide 'customer_id' and 'feedback' list."}), 400

    customer_id = int(customer_id)
    existing_feedback = user_feedback_memory.get(customer_id, [])
    updated_feedback = list(set(existing_feedback + feedback_items))  # Remove duplicates
    user_feedback_memory[customer_id] = updated_feedback

    return jsonify({
        "message": "Feedback received and stored.",
        "customer_id": customer_id,
        "current_feedback": updated_feedback
    })

if __name__ == "__main__":
    app.run(debug=True)