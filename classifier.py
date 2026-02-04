import streamlit as st
from groq import Groq
from prompts import SYSTEM_PROMPT

# Initialize client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Use a valid Groq model ID
MODEL = "llama-3.3-70b-versatile"

def classify_po(po_description: str, supplier: str = "Not provided"):
    user_prompt = f"PO Description:\n{po_description}\n\nSupplier:\n{supplier}"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.0,
            # Ensure your SYSTEM_PROMPT asks for "RAW JSON ONLY"
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"} # Forces JSON mode if supported
        )

        content = response.choices[0].message.content
        
        # Clean up Markdown formatting if the model adds it
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        
        return content

    except Exception as e:
        return f"Error: {str(e)}"
