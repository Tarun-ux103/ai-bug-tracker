import json
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def analyze_code(code, language):

    api_key = os.getenv("GROQ_API_KEY")


    if not api_key:

        return {
            "summary": "Groq API key is missing.",
            "issues": [],
            "error": (
                "GROQ_API_KEY was not found. "
                "Check your .env file."
            )
        }


    try:

        client = Groq(
            api_key=api_key
        )


        prompt = f"""
You are an expert software engineer and AI code reviewer.

Analyze the following {language} source code and identify
potential bugs, security vulnerabilities, logical errors,
missing error handling, and performance problems.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "Short overall analysis summary",
    "issues": [
        {{
            "title": "Issue title",
            "type": "Bug or Security or Logic or Performance",
            "severity": "Low or Medium or High or Critical",
            "description": "Explain the issue",
            "suggested_fix": "Explain how to fix it"
        }}
    ]
}}

If there are no significant issues, return an empty issues list.

Source Code:

{code}
"""


        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise AI code analyzer. "
                        "Always return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )


        result = response.choices[0].message.content

        return json.loads(result)


    except Exception as error:

        return {
            "summary": "Analysis failed.",
            "issues": [],
            "error": str(error)
        }