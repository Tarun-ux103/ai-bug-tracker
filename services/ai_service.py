import json
import os
import re

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def extract_json(response_text):

    # Remove extra spaces
    response_text = response_text.strip()


    # Remove Markdown code blocks if AI returns them
    if response_text.startswith("```"):

        response_text = re.sub(
            r"^```(?:json)?",
            "",
            response_text,
            flags=re.IGNORECASE
        )

        response_text = re.sub(
            r"```$",
            "",
            response_text.strip()
        )


    # Try to find the JSON object
    json_start = response_text.find("{")

    json_end = response_text.rfind("}")


    if json_start != -1 and json_end != -1:

        response_text = response_text[
            json_start:json_end + 1
        ]


    return json.loads(
        response_text
    )


def analyze_code(code, language):

    # Get API key
    api_key = os.getenv(
        "GROQ_API_KEY",
        ""
    ).strip()


    # Check API key
    if not api_key:

        return {
            "summary": "Groq API key is missing.",
            "issues": [],
            "error": (
                "GROQ_API_KEY was not found. "
                "Check your environment variables."
            )
        }


    try:

        # Create Groq client
        client = Groq(
            api_key=api_key
        )


        prompt = f"""
Analyze the following {language} source code.

Find potential:

- Bugs
- Security vulnerabilities
- Logical errors
- Missing error handling
- Performance problems

IMPORTANT:

Return ONLY a valid JSON object.

Do not use Markdown.

Do not use ```json.

Do not add explanations before or after the JSON.

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

If there are no significant issues, return:

{{
    "summary": "No significant issues found.",
    "issues": []
}}

SOURCE CODE:

{code}
"""


        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional AI code analyzer. "
                        "Your response must be valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.1
        )


        result = response.choices[0].message.content
        print("RAW AI RESPONSE:")
        print(result)

        # Check if AI returned a response
        if not result:

            raise ValueError(
                "AI returned an empty response."
            )


        # Convert AI response to JSON
        analysis = extract_json(
            result
        )


        # Ensure required keys exist
        if "summary" not in analysis:

            analysis["summary"] = (
                "Code analysis completed."
            )


        if "issues" not in analysis:

            analysis["issues"] = []


        print(
            "AI analysis completed successfully."
        )


        return analysis


    except json.JSONDecodeError as error:

        print(
            "JSON parsing error:",
            str(error)
        )


        return {
            "summary": (
                "The AI returned an invalid response format."
            ),
            "issues": [],
            "error": (
                "The AI response could not be processed. "
                "Please try analyzing the code again."
            )
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
            "error": str(error)
        }