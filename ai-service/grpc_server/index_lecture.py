import protos.examgen_pb2 
import protos.examgen_pb2_grpc
from db.vector_store import save_chunk,ensure_collection
from Services.embedder import get_embeddings
from Services.chunker import create_chunk

class IndexLecture (protos.examgen_pb2_grpc.ExamAIService):
    @staticmethod
    def IndexLecture(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        try:
            chunks = create_chunk(request.content)

            if not chunks:
                return protos.examgen_pb2.IndexLectureResponse(
                    success=False,
                    error_message="Lecture content is empty",
                    chunks_indexed=0
                )

            embeddings = get_embeddings(chunks)

            count = save_chunk(
                lecture_id=request.lecture_id,
                course_id=request.course_id,
                user_id=request.user_id,
                chunk=chunks,
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
       