import protos.examgen_pb2_grpc
from Services.retrieval import distribute_breakdown, distribute_question, retrivie_lecture_grouped, split_into_groups
import protos.examgen_pb2
from generation.ai_client import generate_exam_questions
from generation.prombtBuilder import build_exam_prompt


class AIExamServicer(protos.examgen_pb2_grpc.ExamAIServiceServicer):

    def GenerateExam(self, request, context):
        try:
            all_groups = []
            for i in request.lectures:
                group = retrivie_lecture_grouped(i.lecture_id, i.questions_count)
                all_groups.extend(group)

            if not all_groups:
                return protos.examgen_pb2.GenerateQuestionsResponse(
                    success=False,
                    error_message="No indexed content found for the selected lectures"
                )

            total_breakdown = {
                "easy": request.difficulty_breakdown.easy,
                "medium": request.difficulty_breakdown.medium,
                "hard": request.difficulty_breakdown.hard
            }
            total_type = {
                "mcq": request.type_breakdown.mcq,
                "true_false": request.type_breakdown.true_false,
                "essay": request.type_breakdown.essay
            }

            groups_count = [x["questions_count"] for x in all_groups]
            breakdown_per_group = distribute_breakdown(total_breakdown, groups_count)
            type_per_group = distribute_breakdown(total_type, groups_count)

            questions = []
            for group, breakdown, q_type in zip(all_groups, breakdown_per_group, type_per_group):
                if group["questions_count"] == 0 or not group["content"]:
                    continue

                prompt = build_exam_prompt(
                    group["content"],
                    group["questions_count"],
                    breakdown,
                    q_type
                )
                question = generate_exam_questions(prompt)
                questions.extend(question)

            response = protos.examgen_pb2.GenerateQuestionsResponse(success=True)
            for q in questions:
                gq = response.questions.add()
                gq.text = q["text"]
                gq.type = q["type"]
                gq.difficulty = q["difficulty"]
                gq.topic = q.get("topic", "")
                gq.explanation = q.get("explanation", "")
                gq.model_answer = q.get("model_answer", "") or ""
                gq.grading_criteria.extend(q.get("grading_criteria", []) or [])
                for opt in q.get("options", []) or []:
                    o = gq.options.add()
                    o.text = opt["text"]
                    o.is_correct = opt["is_correct"]

            return response

        except Exception as e:
            return protos.examgen_pb2.GenerateQuestionsResponse(
                success=False,
                error_message=str(e)
            )