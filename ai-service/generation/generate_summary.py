from groq import Groq
import os
import json
from Services.retrieval import retrieve_context_for_question
FOCUS_POINT_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "submit_focus_point",
        "description": "Submit a focused review point for a weak topic",
        "parameters": {
            "type": "object",
            "properties": {
                "focus_summary": {
                    "type": "string",
                    "description": "A concise, actionable explanation of exactly what the student should focus on, based on their specific mistakes and the reference content. Be as brief as the topic allows — cover only what's necessary, without padding or unnecessary elaboration."
                }
            },
            "required": ["focus_summary"]
        }
    }
}
def build_focus_point_prompt(topic: str, missed_count: int, total_attempted: int, context: str) -> str:
    return f"""A student missed {missed_count} out of {total_attempted} questions on the topic "{topic}".

Based STRICTLY on the reference content below, write a focused review note explaining 
exactly what the student should concentrate on. Do not use any knowledge beyond what's 
provided in the reference content.

Be as concise as the topic allows — cover only what's necessary for the student to 
understand their specific gap. Avoid padding, generic advice, or restating the obvious.

REFERENCE CONTENT (the only source of truth):
{context}

Write the review note in the same language as the reference content above."""

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_exam_summary(topic :str,lecture_id:str,missed:int,total:int)->str:
    context=retrieve_context_for_question(lecture_id,topic,5)
    prompt = build_focus_point_prompt(topic,missed,total,context)
    response =client.chat.completions.create(
        model="openai/gpt-oss-120b", 
        tools=[FOCUS_POINT_TOOL_SCHEMA],
        messages=[{"role": "user", "content": prompt}],
        tool_choice={"type": "function", "function": {"name": "submit_focus_point"}}
    )
    message = response.choices[0].message
    if not message.tool_calls:
        raise Exception ("AI did not return structured focus point")
    argument =json.loads( message.tool_calls[0].function.arguments)
    return argument["focus_summary"]