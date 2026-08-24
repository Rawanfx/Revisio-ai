import protos.examgen_pb2
from generation.prombtBuilder import build_grading_prompt
from Services.retrieval import retrieve_context_for_question
from generation.ai_client import grade_essay_answer

def handle_grade_answer (request):
    try:
        lecture_context = retrieve_context_for_question(request.lecture_id,request.question_text,6)
        if not lecture_context :
            return protos.examgen_pb2.GradeAnswerResponse(
                success=False,
                 error_message="No lecture content found for grading context"
            )
        prompt = build_grading_prompt(
            request.question_text,
            lecture_context,
            request.model_answer,
            request.grading_criteria,
            request.student_answer,
            request.max_score
            )
        result = grade_essay_answer(prompt)
        response = protos.examgen_pb2.GradeAnswerResponse(
            success=True,
            score =result["score"],
            feedback=result["feedback"],
            confidence=result.get("confidence","meduim")
        )
        response.missing_point.extend(result.get("missed_points",[]))
        return response
    except Exception as e:
        response = protos.examgen_pb2.GradeAnswerResponse(
            success=False,
            error_message=str(e)
        )
        return response
