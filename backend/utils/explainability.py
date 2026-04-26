from typing import Dict, List
from utils.llm_client import generate_response


def generate_llm_explanation(prediction: Dict[str, Any], features: Dict[str, float]) -> str:
    context = f"Prediction: {prediction}\nFeatures: {features}"
    query = "Explain this prediction in human-readable terms with cause-effect analysis."
    return generate_response(query, context)


def generate_llm_explanation(data: Dict[str, Any]) -> str:
    context = f"ML Output: {data}"
    query = "Explain this ML prediction result in human-readable terms."
    return generate_response(query, context)

