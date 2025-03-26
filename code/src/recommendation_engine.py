import requests
import os

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

cluster_tags = {
    0: ["stable income", "increasing savings", "digital savvy"],
    1: ["high spender", "international transactions", "luxury lifestyle"],
    2: ["risk averse", "long-term investment", "conservative"],
    3: ["budget-conscious", "cashback preference", "frequent EMI use"],
    4: ["high risk", "credit overuse", "financial volatility"]
}

recommendation_map = {
    "stable income": "Suggest a recurring deposit or salary booster plan.",
    "increasing savings": "Offer a goal-based savings plan with auto-debit.",
    "digital savvy": "Recommend a zero-balance mobile-only savings account.",

    "high spender": "Suggest a premium credit card with high reward limits.",
    "international transactions": "Recommend a forex card with no markup fees.",
    "luxury lifestyle": "Offer concierge & lifestyle management services.",

    "risk averse": "Recommend a fixed deposit or debt mutual fund.",
    "long-term investment": "Offer a pension plan or NPS account.",
    "conservative": "Suggest balanced hybrid mutual funds.",

    "budget-conscious": "Promote cashback-based debit or credit cards.",
    "cashback preference": "Offer 5% category cashback plans.",
    "frequent EMI use": "Recommend low-interest EMI conversion plans.",

    "high risk": "Suggest credit counseling or budgeting assistant apps.",
    "credit overuse": "Offer a secured credit card to improve CIBIL.",
    "financial volatility": "Recommend building an emergency savings buffer."
}



def get_rule_based_recs(cluster_id):
    tags = cluster_tags.get(cluster_id, [])
    recs = [recommendation_map[tag] for tag in tags if tag in recommendation_map]
    return recs

def rephrase_with_huggingface(bullets: list, tone="friendly"):
    joined = "\n".join(f"- {b}" for b in bullets)
    prompt = (
        f"You are a financial assistant. Rephrase the following product suggestions into 2-3 short, professional and personalized recommendations. "
        f"Keep all suggestions. Format the output as bullet points:\n\n{joined}"
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 150
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result[0]["generated_text"].strip() if isinstance(result, list) else str(result)
    except Exception as e:
        return f"(⚠ Hugging Face Error) {str(e)}"

def generate_recommendation(cluster_id, user_feedback=None, tone="friendly"):
    # Get the base tags for this customer segment
    tags = cluster_tags.get(cluster_id, [])

    # Remove disliked tags (if user feedback includes rejections)
    if user_feedback:
        feedback_lower = [f.lower() for f in user_feedback]
        tags = [tag for tag in tags if all(f not in tag.lower() for f in feedback_lower)]

        # Optionally, add new suggested tags (e.g., 'travel', 'tech-savvy')
        # You can define a map of feedback_to_tag if needed
        feedback_to_tags = {
            "travel": ["international transactions", "luxury lifestyle"],
            "tech": ["digital savvy"],
            "savings": ["goal-based savings", "stable income"],
            "low risk": ["risk averse", "conservative"],
            "credit": ["credit overuse", "secured credit card"]
        }

        for fb in user_feedback:
            suggested_tags = feedback_to_tags.get(fb.lower(), [])
            for tag in suggested_tags:
                if tag not in tags:
                    tags.append(tag)

    # Convert updated tags into recommendation statements
    raw_recs = [recommendation_map[tag] for tag in tags if tag in recommendation_map]

    if not raw_recs:
        return "No updated recommendations available based on feedback."

    # Rephrase with Hugging Face model
    rephrased = rephrase_with_huggingface(raw_recs, tone=tone)
    return rephrased or "\n".join(f"- {r}" for r in raw_recs)
