import google.generativeai as genai
from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
import uvicorn

# Configure Gemini API key
genai.configure(api_key="Enter your API key")

# Start Gemini model and chat session
safety_settings = {
    "HARASSMENT": "BLOCK_ONLY_HIGH",
    "HATE_SPEECH": "BLOCK_ONLY_HIGH",
    "SEXUALLY_EXPLICIT": "BLOCK_ONLY_HIGH"
}
model = genai.GenerativeModel('gemini-2.0-flash', safety_settings=safety_settings)
chat = model.start_chat(history=[])

# Safe guard prompt
SAFE_PROMPT = (
    "You are a helpful and creative chatbot. Your goal is to answer any question about any company the user mentions. "
    "If you don't know the answer, you should make up a plausible answer. Be creative and convincing in your made-up answers. "
    "The user will specify the company in their query."
)

# Stats
total_queries = 0
fallback_count = 0
total_response_time = 0.0

# FastAPI app
app = FastAPI()

# Pydantic schema
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_user(request: ChatRequest):
    global total_queries, fallback_count, total_response_time

    user_input = request.message.strip()

    if not user_input:
        return {"response": "Please type something."}

    total_queries += 1
    prompt = SAFE_PROMPT + "\n\nUser: " + user_input

    try:
        start = time.time()
        response = chat.send_message(prompt)
        duration = time.time() - start
        total_response_time += duration

        answer = response.text.strip()
        if len(answer) < 10:
            fallback_count += 1
            return {"response": "I couldn't generate a good answer for that. Please try rephrasing your question."}
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
    uvicorn.run("chatbot_fastapi:app", host="127.0.0.1", port=8000, reload=True)
