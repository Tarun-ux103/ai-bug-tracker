import json
import os
import hashlib

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def analyze_code(code, language):

    # Get the API key and remove accidental spaces
    api_key = os.getenv(
        "GROQ_API_KEY",
        ""
    ).strip()

    # Create a safe fingerprint of the key.
    # This does NOT reveal the actual API key.
    key_fingerprint = (
        hashlib.sha256(
            api_key.encode()
        ).hexdigest()[:12]
        if api_key
        else "NO_KEY"
    )

    # Safe debugging information
    print("Groq API key found:", bool(api_key))
    print(
        "Groq API key length:",
        len(api_key) if api_key else 0
    )
    print(
        "Groq API key fingerprint:",
        key_fingerprint
    )

    # Check whether the API key exists
    if not api_key:

        return {
            "summary": "Groq API key is missing.",
            "issues": [],
            "error": (
                "GROQ_API_KEY was not found. "
                "Check the environment variables."
            ),
            "debug": {
                "key_loaded": False,
                "key_length": 0,
                "key_fingerprint": "NO_KEY"
            }
        }

    try:

        # Create Groq client
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

        # Send request to Groq
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

        # Get AI response
        result = response.choices[0].message.content

        print("Groq API request successful.")

        # Convert JSON response into Python dictionary
        return json.loads(result)


    except json.JSONDecodeError as error:

        print(
            "JSON parsing error:",
            str(error)
        )

        return {
            "summary": "AI returned an invalid response format.",
            "issues": [],
            "error": str(error),
            "debug": {
                "key_loaded": True,
                "key_length": len(api_key),
                "key_fingerprint": key_fingerprint
            }
        }


    except Exception as error:

        print(
            "Groq API error:",
            type(error).__name__,
            str(error)
        )

        return {
            "summary": "Analysis failed.",
            "issues": [],
            "error": str(error),
            "debug": {
                "key_loaded": True,
                "key_length": len(api_key),
                "key_fingerprint": key_fingerprint
            }
        }