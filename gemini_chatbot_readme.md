# Gemini Safe Chatbot API

This project is a **FastAPI-based chatbot API** integrated with **Google Gemini (generative AI)** to create a professional, safe, and company-specific conversational interface.

## Features

- Restricts responses to company services, contact, and location
- Filters banned or inappropriate words
- Returns fallback responses for unrelated queries
- Tracks usage metrics: total queries, fallbacks, average response time
- Exposes two endpoints: `/chat` and `/metrics`

---

## Prerequisites

- Python 3.8+ installed
- Google Gemini API key (from [Google AI Studio](https://aistudio.google.com/))

Install dependencies:

```bash
pip install google-generativeai fastapi pydantic uvicorn
```

---

## Project Structure

```
chatbot_api.py
README.md
```

---

## Setup and Running

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/gemini-safe-chatbot-api.git
   cd gemini-safe-chatbot-api
   ```

2. **Add your Gemini API key**

   In `chatbot_api.py`, replace:

   ```python
   genai.configure(api_key="Add your API Key")
   ```

   with:

   ```python
   genai.configure(api_key="YOUR_ACTUAL_API_KEY")
   ```

3. **Run the FastAPI server**

   ```bash
   uvicorn chatbot_api:app --reload
   ```

4. **Test the endpoints**

   - **POST /chat** with JSON body:

     ```json
     { "message": "Hello, what services do you offer?" }
     ```

   - **GET /metrics** to view usage statistics.

---

## Code Overview

### 1. Imports and Configuration

- Uses `google.generativeai` to connect to Gemini.
- Initializes FastAPI and loads the Gemini model (`gemini-2.0-flash`).

### 2. Safe Prompt

A fixed `SAFE_PROMPT` ensures the chatbot only answers company-related queries, returning a fallback otherwise.

### 3. Banned Words

A list of blocked words (`BANNED_WORDS`) to ensure professionalism.

### 4. Endpoints

- **POST /chat**

  - Validates user input.
  - Checks for banned words.
  - Sends a prompt to Gemini, including safe instructions.
  - Returns fallback for unrelated or unsafe responses.

- **GET /metrics**

  - Returns:
    - Total queries
    - Fallback count
    - Average response time

### 5. Running Condition

The script runs with:

```python
if __name__ == "__main__":
    uvicorn.run("chatbot_api:app", host="127.0.0.1", port=8000, reload=True)
```

---

## Notes

- Ensure your API key has **Gemini model access**.
- Extend `BANNED_WORDS` as per your organization's content policy.
- The current implementation stores metrics in memory; for production, integrate with a persistent database or monitoring system.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

[**Your Name**](https://github.com/yourusername)\
Feel free to reach out for suggestions, improvements, or collaboration ideas.

---

Let me know if you want a **requirements.txt**, **Dockerfile**, or GitHub Actions CI/CD YAML ready for this project today.

