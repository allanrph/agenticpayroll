import json
import os
import time
from typing import Dict, Any
from google import genai
from google.genai import types
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.adapters.llm.llm_client_interface import ILLMClient


class LLMSettings(BaseSettings):
    """LLM configuration settings."""

    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    max_retries: int = 3
    retry_delay: int = 2  # seconds

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GeminiLLMClient(ILLMClient):
    """Gemini LLM client implementation following project patterns."""

    def __init__(self, settings: LLMSettings):
        self.settings = settings
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Gemini client."""
        try:
            self._client = genai.Client(api_key=self.settings.gemini_api_key)
        except Exception as e:
            print(
                f"Error initializing Gemini client: {e}. Please ensure API key is set."
            )
            self._client = None

    async def run_crew_agent(
        self, role: str, instructions: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes a single step of the payroll crew by calling the LLM with a specialized role.
        The LLM receives the full current state (data) and returns the modified state.
        """
        for attempt in range(self.settings.max_retries):
            try:
                if not self._client:
                    return {"error": "LLM client not initialized."}

                system_message = (
                    f"You are the {role}. Your task is to ONLY perform the specified calculation based on the provided data "
                    "and append the results to the 'Calculated_Components' section of the output JSON. "
                    "You MUST return the entire updated JSON data structure, ensuring all existing keys are preserved."
                )

                user_prompt = f"""
                --- CURRENT PAYROLL STATE (JSON INPUT) ---
                {json.dumps(data, indent=2)}
                
                --- INSTRUCTIONS FOR YOUR ROLE ---
                {instructions}
                
                Your output MUST be a complete JSON object adhering to the structure of the input.
                """

                # --- GEMINI API Call Structure ---
                response = self._client.models.generate_content(
                    model=self.settings.gemini_model,
                    contents=[
                        {
                            "role": "user",
                            "parts": [{"text": system_message + user_prompt}],
                        }
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.1, response_mime_type="application/json"
                    ),
                )

                # The response is the full, updated payroll state (JSON)
                return json.loads(response.text)

            except Exception as e:
                if (
                    "503 UNAVAILABLE" in str(e)
                    and attempt < self.settings.max_retries - 1
                ):
                    print(
                        f"[{role}]: Service unavailable, 503 Overload. Retrying in {self.settings.retry_delay} seconds..."
                    )
                    time.sleep(self.settings.retry_delay)
                    continue

                return {"error": f"API_FAILURE", "details": str(e)}

        return {
            "error": f"{role}_FAILURE",
            "details": "All retry attempts failed due to service overload (503).",
        }
