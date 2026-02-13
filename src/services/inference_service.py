import os
import joblib
import pandas as pd
from src.preprocessing.text_cleaner import clean_text

# Get project root dynamically
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

MODELS_DIR = os.path.join(BASE_DIR, "models")

category_model = joblib.load(os.path.join(MODELS_DIR, "category_model.pkl"))
sentiment_model = joblib.load(os.path.join(MODELS_DIR, "support_sentiment_model.pkl"))
escalation_model = joblib.load(os.path.join(MODELS_DIR, "escalation_model.pkl"))
feature_columns = joblib.load(os.path.join(MODELS_DIR, "escalation_feature_columns.pkl"))



def predict_ticket(ticket: dict) -> dict:
    """
    Unified AI inference pipeline.
    """

    # 1️ Clean and prepare text
    combined_text = f"{ticket['subject']} {ticket['description']}"
    cleaned = clean_text(combined_text)

    # 2️ Predict category
    predicted_category = category_model.predict([cleaned])[0]

    # 3️ Predict support sentiment
    predicted_sentiment = sentiment_model.predict([cleaned])[0]

    # 4️ Prepare structured features for escalation
    structured_input = pd.DataFrame([{
        "category": predicted_category,
        "priority": ticket["priority"],
        "customer_plan": ticket["customer_plan"],
        "support_sentiment": predicted_sentiment,
        "sla_breached": ticket["sla_breached"]
    }])

    structured_input = pd.get_dummies(structured_input)

    # Align columns with training
    structured_input = structured_input.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # 5️ Predict escalation probability
    escalation_prob = escalation_model.predict_proba(structured_input)[0][1]
    escalation_flag = int(escalation_prob > 0.5)

    return {
        "predicted_category": predicted_category,
        "predicted_support_sentiment": predicted_sentiment,
        "escalation_probability": round(float(escalation_prob), 3),
        "escalation_flag": escalation_flag
    }
