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
                                "type": ["array","null"],
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





GRADING_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "submit_grading",
        "description": "Submit the grading result for a student's essay answer",
        "parameters": {
            "type": "object",
            "properties": {
                "score": {"type": "number", "description": "Score out of max_score"},
                "feedback": {"type": "string", "description": "Explanation of the grade, in the student's language"},
                "missed_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Key points the student missed"
                },
                "confidence": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "How confident you are in this grading based on the reference material"
                }
            },
            "required": ["score", "feedback", "confidence"]
        }
    }
}


def grade_essay_answer(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        tools=[GRADING_TOOL_SCHEMA],
        tool_choice={"type": "function", "function": {"name": "submit_grading"}}
    )

    message = response.choices[0].message
    if not message.tool_calls:
        raise Exception("AI did not return grading result")

    return json.loads(message.tool_calls[0].function.arguments)