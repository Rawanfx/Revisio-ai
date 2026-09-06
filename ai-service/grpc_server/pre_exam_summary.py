from generation.generate_summary import generate_exam_summary
from protos import examgen_pb2
def handle_pre_exam_summary(request):
    reviews=[]
    try:
         for wt in request.weak_topics :
                focus_point = generate_exam_summary(request.topic,request.lecture_id,request.missed_count,request.total_attempted)
                reviews.append(examgen_pb2.TopicReview(
                    lecture_id = wt.lecture_id,
                    topic = wt.topic,
                    focus_point=focus_point
                ))
         return examgen_pb2.GenerateSummaryResponse(
                success=True,
                reviews=reviews
            ) 
    except Exception as e:
      return examgen_pb2.GenerateSummaryResponse(
                success=True,
                error_message=str(e)
      )
    