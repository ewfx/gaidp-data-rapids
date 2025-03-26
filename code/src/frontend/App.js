import React, { useState } from "react";
import axios from "axios";

function App() {
  const [customerId, setCustomerId] = useState("");
  const [recommendation, setRecommendation] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [message, setMessage] = useState("");

  const getRecommendation = async () => {
    try {
      const res = await axios.get(`http://127.0.0.1:5000/recommend?customer_id=${customerId}`);
      setRecommendation(res.data);
      setMessage("");
    } catch (error) {
      setMessage("Could not fetch recommendation.");
    }
  };

  const sendFeedback = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/feedback", {
        customer_id: Number(customerId),
        feedback: feedback.split(",").map(f => f.trim())
      });
      setMessage("Feedback sent! Refresh recommendations.");
    } catch (error) {
      setMessage("Error sending feedback.");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>📊 Personalized Financial Recommendations</h2>

      <input
        type="number"
        placeholder="Enter Customer ID"
        value={customerId}
        onChange={(e) => setCustomerId(e.target.value)}
      />
      <button onClick={getRecommendation}>Get Recommendation</button>

      {recommendation && (
        <div style={{ marginTop: 20 }}>
          <h3>Recommendation for Customer #{recommendation.customer_id}</h3>
          <p><strong>Cluster:</strong> {recommendation.cluster_id}</p>
          <p><strong>Personalized:</strong><br />{recommendation.personalized_recommendation}</p>
          <p><strong>Engagement Strategy:</strong> {recommendation.engagement_strategy}</p>
          <p><strong>Product Discovery:</strong> {recommendation.product_discovery}</p>
          <p><strong>Service Optimization:</strong> {recommendation.service_optimization}</p>

          <h4>🚫 Didn't like something? Give Feedback</h4>
          <input
            type="text"
            placeholder="e.g. fixed deposit, too conservative"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
          <button onClick={sendFeedback}>Submit Feedback</button>
        </div>
      )}

      {message && <p style={{ marginTop: 20, color: "green" }}>{message}</p>}
    </div>
  );
}

export default App;
