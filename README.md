# ⚡ Prompt Optimization Platform

A **Flask**-based web tool that takes a raw user prompt and uses **Google Gemini** to rewrite it into a clearer, more specific, and more effective prompt for downstream LLM use.

---

## ✨ Features

- **Simple web UI** (`templates/index.html`) — dark-themed, single-page interface with a textarea for the input prompt and a results panel.
- **Prompt optimization endpoint** — sends the user's prompt to Gemini with an instruction to improve clarity and specificity, returning the rewritten version.
- **Reusable `GeminiService` class** (`services/gemini_service.py`) that wraps the Gemini client for general-purpose text generation and prompt optimization, configurable with temperature and max token limits.
- **Centralized configuration** (`config.py`) that loads the Gemini API key and database path from environment variables.
- Includes a secondary template (`templates/optimize.html`) for a traditional form-based (server-rendered) optimization flow.

---

## 🗂️ Project Structure

```
Prompt_Optimization_Platform/
├── app.py                        # Main Flask app: home page + /optimize endpoint
├── config.py                       # Loads GEMINI_API_KEY and DB_PATH from .env
├── requirements.txt                  # Python dependencies
├── services/
│   └── gemini_service.py              # GeminiService class: generate() and optimize_prompt()
├── templates/
│   ├── index.html                      # Main dark-themed single-page UI (JS-driven)
│   └── optimize.html                    # Alternate server-rendered form UI
└── .env                                  # API key / DB path configuration (not committed)
```

---

## ⚙️ Requirements

- Python 3.9+
- A **Google Gemini API key**

Dependencies (see `requirements.txt`):

```
flask
flask-sqlalchemy
python-dotenv
sqlalchemy
google-generativeai
```

> Note: `app.py` and `services/gemini_service.py` use the newer `google-genai` client (`from google import genai`). Ensure the `google-genai` package is installed alongside/instead of `google-generativeai` if you hit import errors — see [Notes](#️-notes) below.

---

## 🔧 Setup

1. **Navigate into the project folder:**
   ```bash
   cd Prompt_Optimization_Platform
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install google-genai       # required by app.py / gemini_service.py
   ```

3. **Configure environment variables.** Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DB_PATH=prompts_db.sqlite
   ```

---

## ▶️ Usage

Run the Flask development server:

```bash
python app.py
```

The app will be available at:

```
http://localhost:5000
```

In the browser:

1. Enter your draft prompt into the textarea.
2. Click **Optimize Prompt**.
3. The improved, more effective version of your prompt will appear in the results panel.

---

## 🔌 API Reference

### `POST /optimize`

Optimizes a given prompt using Gemini.

**Request body:**
```json
{ "prompt": "write me something about dogs" }
```

**Response (success):**
```json
{ "optimized": "Write a 300-word, engaging article about the history and behavior of domestic dogs, aimed at a general audience..." }
```

**Response (error):**
```json
{ "error": "Description of the error" }
```

---

## 🧠 How It Works

1. The front end (`index.html`) posts the user's raw prompt as JSON to `/optimize`.
2. `app.py` calls `client.models.generate_content()` with model `gemini-2.5-flash`, wrapping the user's prompt in an instruction: *"Optimize this prompt for better LLM results: ..."*.
3. The optimized prompt text is returned as JSON and rendered in the results panel.
4. Separately, `services/gemini_service.py` provides a more structured `GeminiService` class with:
   - `generate(prompt, temperature, max_tokens)` — general-purpose content generation.
   - `optimize_prompt(prompt)` — a dedicated method that rewrites a prompt for clarity, specificity, and effectiveness (temperature `0.4`).

---

## 🛠️ Tech Stack

| Component        | Technology                         |
|--------------------|---------------------------------------|
| Backend             | Flask                                  |
| LLM                 | Google Gemini (`gemini-2.5-flash`)      |
| Frontend            | Server-rendered HTML + vanilla JS        |
| Config management     | python-dotenv                              |
| ORM (available)         | Flask-SQLAlchemy / SQLAlchemy (for future prompt history persistence) |

---

## ⚠️ Notes

- `config.py` raises a `ValueError` at import time if `GEMINI_API_KEY` is missing from `.env` — make sure it's set before running.
- `services/gemini_service.py` defaults to a `model_name` of `"gemini-3.5-flash"` if none is passed in, while `app.py` explicitly uses `"gemini-2.5-flash"` — verify which Gemini model versions are available to your API key and adjust as needed.
- `flask-sqlalchemy` / `sqlalchemy` and `DB_PATH` are present in the config/dependencies for future persistence of prompt history, but no database models or storage logic are implemented yet in `app.py`.
- `templates/optimize.html` expects a Flask route that accepts `POST` with a `prompt` form field and renders a `result` variable — this route is not present in the current `app.py` and would need to be added to use that page.

---

## 📄 License

This project is provided as-is for educational and personal use. Add a license of your choice before distributing.
