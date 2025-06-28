import google.generativeai as genai
from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
import uvicorn

# Configure Gemini API key
genai.configure(api_key="AIzaSyBz8txRId0M_sd-qfnXKo9QRZ3TO5gm6ow")

# Start Gemini model and chat session
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])

# Safe guard prompt and banned words
SAFE_PROMPT = (
    "You are a safe, professional chatbot. Only answer questions about our company's services, contact, or location. "
    "If the question is unrelated, say: 'I'm not sure about that. Please contact our support team.'"
)
BANNED_WORDS = ["idiot", "hate", "stupid", "kill", "dumb", "looser"]

# Stats
total_queries = 0
fallback_count = 0
total_response_time = 0.0

# FastAPI app
app = FastAPI()

# Pydantic schema
class ChatRequest(BaseModel):
    message: str

def contains_banned_words(text):
    return any(word in text.lower() for word in BANNED_WORDS)

@app.post("/chat")
async def chat_with_user(request: ChatRequest):
    global total_queries, fallback_count, total_response_time

    user_input = request.message.strip()

    if not user_input:
        return {"response": "Please type something."}

    if contains_banned_words(user_input):
        return {"response": "Inappropriate language detected. Please rephrase."}

    total_queries += 1
    prompt = SAFE_PROMPT + "\n\nUser: " + user_input

    try:
        start = time.time()
        response = chat.send_message(prompt)
        duration = time.time() - start
        total_response_time += duration

        answer = response.text.strip()
        if "I'm not sure" in answer or len(answer) < 10:
            fallback_count += 1
            return {"response": "I'm not sure about that. Please contact our support team."}
        else:
            return {"response": answer}

    except Exception as e:
        return {"response": f"Error occurred: {str(e)}"}

@app.get("/metrics")
def metrics():
    avg_time = round(total_response_time / total_queries, 2) if total_queries else 0
    return {
        "total_queries": total_queries,
        "fallbacks": fallback_count,
        "average_response_time_seconds": avg_time
    }

# To run this: uvicorn chatbot_api:app --reload
if __name__ == "__main__":
    uvicorn.run("chatbot_api:app", host="127.0.0.1", port=8000, reload=True)
