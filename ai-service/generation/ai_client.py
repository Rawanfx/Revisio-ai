from groq import Groq
import os
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


EXAM_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "submit_generated_exam",
        "description": "Submit the generated exam questions",
        "parameters": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "type": {"type": "string", "enum": ["MCQ", "TrueFalse", "Essay"]},
                            "difficulty": {"type": "string", "enum": ["Easy", "Medium", "Hard"]},
                            "topic": {"type": "string"},
                            "explanation": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "text": {"type": "string"},
                                        "is_correct": {"type": "boolean"}
                                    },
                                    "required": ["text", "is_correct"]
                                }
                            },
                            "model_answer": {"type": ["string","null"]},
                            "grading_criteria": {
                                "type": ["array","null"],
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["text", "type", "difficulty", "topic", "explanation"]
                    }
                }
            },
            "required": ["questions"]
        }
    }
}


def generate_exam_questions(prompt: str) -> list[dict]:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b", 
        messages=[{"role": "user", "content": prompt}],
        tools=[EXAM_TOOL_SCHEMA],
        tool_choice={"type": "function", "function": {"name": "submit_generated_exam"}}
    )

    message = response.choices[0].message

    if not message.tool_calls:
        raise Exception("AI did not return structured questions")

    arguments = json.loads(message.tool_calls[0].function.arguments)
    return arguments["questions"]