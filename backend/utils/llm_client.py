import openai
from config import Config

client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_reasoned_response(query: str, context: str = "") -> str:
    system_prompt = "You are a fleet AI system making decisions. Analyze the context, provide reasoning, and give a final answer."
    user_prompt = f"Context: {context}\n\nQuery: {query}\n\nProvide reasoning and final answer."
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()