import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = OPENAI_API_KEY)

def get_ai_response(prompt, model="gpt-3.5-turbo"):
    system_prompt = "당신은 학생들을 돕는 유능한 학습 도우미입니다. 정확하고 이해하기 쉬운 설명을 제공하세요."
    try:
        response = client.responses.create(
            model=model,
            instructions=system_prompt,
            input = prompt
        )
        return response.output_text
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"