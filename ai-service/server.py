from dotenv import load_dotenv
load_dotenv()
import grpc
from concurrent import futures
import protos.examgen_pb2
import protos.examgen_pb2_grpc
from db.vector_store import ensure_collection, save_chunk
from grpc_server.generate_exam import GenerateExam
from grpc_server.index_lecture import handle_index_lecture
from grpc_server.grade_answer_handle import handle_grade_answer
class ExamAIServicer(protos.examgen_pb2_grpc.ExamAIServiceServicer):

    def IndexLecture(self, request, context):
       return handle_index_lecture(request)

    def GenerateExam(self, request, context):
       return GenerateExam(request)

    def GradeAnswer(self, request, context):
        return handle_grade_answer(request)

    def GradeImageAnswer(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        return protos.examgen_pb2.GradeAnswerResponse()

    def ExplainConcept(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        return protos.examgen_pb2.ExplainConceptResponse()


def serve():
    
    ensure_collection()  
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protos.examgen_pb2_grpc.add_ExamAIServiceServicer_to_server(ExamAIServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("AI service running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()