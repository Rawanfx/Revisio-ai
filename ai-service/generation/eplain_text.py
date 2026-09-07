import json
from Services.retrieval import retrieve_context_for_question
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EXPLAIN_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "submit_explanation",
        "description": "Submit an expanded explanation for a selected concept",
        "parameters": {
            "type": "object",
            "properties": {
                "expanded_explanation": {
                    "type": "string",
                    "description": "A clear, expanded explanation of the selected concept, grounded strictly in the reference content."
                },
                "real_example": {
                    "type": ["string", "null"],
                    "description": "A concrete, real example illustrating the concept, drawn from or consistent with the reference content. Return null if no suitable example can be grounded in the reference content."
                }
            },
            "required": ["expanded_explanation"]
        }
    }
}

def build_explain_prompt(selected_text: str, question_context: str, source_context: str) -> str:
    return f"""A student is reviewing this question and didn't fully understand a specific part.

QUESTION CONTEXT: {question_context}

TEXT THE STUDENT SELECTED (needs more explanation): "{selected_text}"

Based STRICTLY on the reference content below:
1. Write an expanded explanation of the selected concept.
2. If the reference content supports a concrete real-world example, provide one. 
   If not, leave the example empty rather than inventing one.

Do not use any knowledge beyond what's provided in the reference content.

REFERENCE CONTENT:
{source_context}

Write in the same language as the reference content."""


def generate_explain_text(selected_text: str, question_text: str, lecture_id: str) -> dict:
    context = retrieve_context_for_question(lecture_id=lecture_id, question_text=selected_text, top_k=5)
    
    if not context:
        return {"expanded_explanation": "", "real_example": None}
    
    prompt = build_explain_prompt(selected_text, question_text, context)
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        tools=[EXPLAIN_TOOL_SCHEMA],
        messages=[{"role": "user", "content": prompt}],
        tool_choice={"type": "function", "function": {"name": "submit_explanation"}}
    )
    
    message = response.choices[0].message
    if not message.tool_calls:
        raise Exception("AI did not return structured explanation")
    
    arguments = json.loads(message.tool_calls[0].function.arguments)
    return {
        "expanded_explanation": arguments["expanded_explanation"],
        "real_example": arguments.get("real_example")
    }