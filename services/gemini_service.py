import os
from google import genai
from google.genai import types


class GeminiService:
    def __init__(self, api_key: str | None = None, model_name: str = "gemini-3.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int | None = None) -> str:
        config = types.GenerateContentConfig(
            temperature=temperature,
        )
        if max_tokens is not None:
            config.max_output_tokens = max_tokens

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )

        return response.text or ""

    def optimize_prompt(self, prompt: str) -> str:
        optimize_text = (
            "Rewrite this prompt to be clearer, more specific, and more effective:\n\n"
            f"{prompt}"
        )
        return self.generate(optimize_text, temperature=0.4)