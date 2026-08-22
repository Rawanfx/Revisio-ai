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


def build_grading_prompt(question_text, lecture_context, model_answer, grading_criteria, student_answer, max_score):
    criteria_text = "\n".join(f"- {c}" for c in grading_criteria) if grading_criteria else "No specific criteria provided."

    return f"""You are grading a student's answer STRICTLY based on the lecture content below.
Do NOT use external/general knowledge beyond what's provided here.
If the lecture content doesn't fully address a point, note that explicitly rather than
filling gaps from your own knowledge.

QUESTION:
{question_text}

LECTURE CONTENT (the primary source of truth for grading):
{lecture_context}

REFERENCE ANSWER (a summary guide, not exhaustive — use the lecture content above as the main authority):
{model_answer}

EXPECTED KEY POINTS:
{criteria_text}

STUDENT ANSWER:
{student_answer}

MAX SCORE: {max_score}

Grade the student's answer based primarily on the LECTURE CONTENT above.
If the student's answer contains correct information from the lecture that isn't
mentioned in the reference answer, still give credit for it.
Return your evaluation using the submit_grading tool."""