import asyncio
from google import genai
import os
import dotenv

dotenv.load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is not found.")
        self.client = genai.Client(api_key=api_key)

    async def generate(self, prompt):
        def _generate():
            response = self.client.models.generate_content(
                model = "gemini-2.5-flash",
                contents = prompt
            )
            return response.text
        return await asyncio.to_thread(_generate)

    
if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    print(GeminiClient().generate(prompt))