import grpc
from concurrent import futures
import protos.examgen_pb2
import protos.examgen_pb2_grpc
from Services.embedder import get_embeddings
from Services.indexing import chunk_text
from db.vector_store import ensure_collection, save_chunks


class ExamAIServicer(protos.examgen_pb2_grpc.ExamAIServiceServicer):

    def IndexLecture(self, request, context):
        try:
            chunks = chunk_text(request.content)

            if not chunks:
                return protos.examgen_pb2.IndexLectureResponse(
                    success=False,
                    error_message="Lecture content is empty",
                    chunks_indexed=0
                )

            embeddings = get_embeddings(chunks)

            count = save_chunks(
                lecture_id=request.lecture_id,
                course_id=request.course_id,
                user_id=request.user_id,
                chunks=chunks,
                embeddings=embeddings
            )

            return protos.examgen_pb2.IndexLectureResponse(
                success=True,
                error_message="",
                chunks_indexed=count
            )

        except Exception as e:
            return protos.examgen_pb2.IndexLectureResponse(
                success=False,
                error_message=str(e),
                chunks_indexed=0
            )

    def GenerateExam(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        return protos.examgen_pb2.GenerateQuestionsResponse()

    def GradeAnswer(self, request, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        return protos.examgen_pb2.GradeAnswerResponse()

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