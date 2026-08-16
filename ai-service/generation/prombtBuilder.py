def build_exam_prompt(content: str, questions_count: int,
                       difficulty_breakdown: dict, type_breakdown: dict) -> str:
    return f"""You are an exam generator for university-level educational content.
Generate exactly {questions_count} questions based STRICTLY on the content provided below.
Do not use any information outside the provided content.

DIFFICULTY DISTRIBUTION:
- Easy: {difficulty_breakdown['easy']}
- Medium: {difficulty_breakdown['medium']}
- Hard: {difficulty_breakdown['hard']}

QUESTION TYPE DISTRIBUTION:
- MCQ: {type_breakdown['mcq']}
- Essay: {type_breakdown['essay']}
- TrueFalse: {type_breakdown['true_false']}

CONTENT:
{content}

Requirements per question type:
- MCQ: exactly 4 options, exactly one marked as correct (is_correct: true)
- TrueFalse: exactly 2 options, exactly one marked as correct (is_correct: true)
- Essay: no options; MUST include a model_answer (the correct/ideal answer) 
  and 2-4 grading_criteria points

CRITICAL: Every question must have a clear, verifiable correct answer.
For MCQ/TrueFalse, this means exactly one option with is_correct: true.
For Essay, this means a complete model_answer field — never leave it empty.

IMPORTANT: Write the question text, options, explanations, and all content
in the SAME language as the source content above (do not translate).
If the content is in Arabic, respond entirely in Arabic. If English, respond in English."""