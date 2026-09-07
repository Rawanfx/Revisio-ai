from protos import examgen_pb2
from generation.eplain_text import generate_explain_text

def handle_explain_text(request):
   try :
       result = generate_explain_text(request.selected_text,request.question_text,request.lecture_id)
       return examgen_pb2.ExplainConceptResponse(
           success=True,
           explanation=result.get("expanded_explanation"),
           real_example = result.get("real_example") or ""
        )
   except Exception as e:
       return examgen_pb2.ExplainConceptResponse(
           success=False,
           error_message=str(e)
       )
