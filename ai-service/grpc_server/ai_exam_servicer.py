import protos.examgen_pb2_grpc
from Services.retrieval import distribute_breakdown,distribute_question,retrivie_lecture_grouped,split_into_groups
import protos.examgen_pb2 
from generation.prombtBuilder import build_exam_prompt
class AIExamServicer(protos.examgen_pb2_grpc.ExamAIServiceServicer):
    def GenerateExam(self, request, context):
        all_groups =[]
        for i in request.lectures:
            group = retrivie_lecture_grouped(i.lecture_id,i.questions_count)
            all_groups.extend(group)
        total_breakdown = {
            "easy":request.difficulty_breakdown.easy,
            "medium":request.difficulty_breakdown.medium,
            "hard":request.difficulty_breakdown.hard
        }
        total_type = {
            "mcq":request.type_breakdown.mcq,
            "true_false":request.type_breakdown.true_false,
            "essay":request.type_breakdown.essay
        }
        groups_count=[x["questions_count"] for x in all_groups]
        breakdown_per_group = distribute_breakdown(total_breakdown,groups_count)
        type_per_group = distribute_breakdown(total_type,groups_count)
        for group,breakdown,type in zip (all_groups,breakdown_per_group,type_per_group):
            prombt = build_exam_prompt(
                group["content"],
                group["questions_count"],
                breakdown,
                type
            )
            
