# Revisio AI Service

An AI-powered microservice for intelligent exam generation, automated essay grading, concept explanation, and personalized exam preparation. Built with Python, gRPC, Retrieval-Augmented Generation (RAG), Qdrant, and Groq.

This service is part of **Revisio AI**, an educational platform designed to help students practice, understand lecture content, and improve their learning experience through AI-powered features.

## 🚀 Features

- **📚 Lecture Indexing:** Processes lecture content, splits it into smaller chunks, generates embeddings, and stores them in Qdrant for efficient retrieval.
- **📝 AI Exam Generation:** Generates multiple-choice questions (MCQs), true/false questions, and essay questions based on selected lecture content.
- **🎯 Automated Essay Grading:** Evaluates students' answers against lecture content, model answers, and grading criteria, providing scores, feedback, and missing key points.
- **💡 Concept Explanation:** Provides expanded explanations of selected concepts and relevant real-world examples grounded in the lecture material.
- **📖 Personalized Exam Preparation:** Generates focused revision notes for topics where students have demonstrated weaknesses.
- **🔎 Retrieval-Augmented Generation (RAG):** Retrieves relevant lecture content to ground AI-generated responses in the learning material.
- **⚡ gRPC Communication:** Exposes a gRPC service for communication with other components of the application.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core service implementation |
| gRPC | Communication between application services |
| Protocol Buffers | Defines service contracts and request/response messages |
| Qdrant | Vector database for storing and retrieving lecture embeddings |
| Sentence Transformers | Converts lecture chunks into vector embeddings |
| Hugging Face Transformers | Tokenization for text chunking |
| LangChain Text Splitters | Splits lecture content into manageable chunks |
| Groq API | Runs the language model for AI-powered features |
| Docker Compose | Runs the Qdrant vector database |
| python-dotenv | Loads environment variables |

### AI Models

- **Language model:** `openai/gpt-oss-120b` through the Groq API.
- **Embedding model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

The embedding model supports multilingual text, making it suitable for educational content in languages such as Arabic and English.

## 🏗️ Architecture

The service follows a modular architecture that separates gRPC request handling, retrieval, vector storage, and AI generation.

```text
                  Application / Client
                          |
                          | gRPC
                          v
                  +------------------+
                  |   gRPC Server    |
                  |    server.py     |
                  +------------------+
                          |
             +------------+-------------+
             |            |             |
             v            v             v
       Lecture Index   Retrieval    AI Generation
             |            |             |
             v            v             v
          Chunking    Query Qdrant   Groq API
             |            |             |
             v            v             |
         Embeddings   Relevant Context |
             |            |             |
             v            +-------------+
          Qdrant              |
                              v
                      AI-Generated Result
                              |
                              v
                       gRPC Response
```

## 🧠 Retrieval-Augmented Generation (RAG)

RAG is a core component of this service. It allows the AI to generate responses using relevant information retrieved from the actual lecture material rather than relying solely on the language model's pretrained knowledge.

### 1. Lecture Indexing

When a lecture is submitted for indexing:

1. The service receives the lecture content and its associated lecture, course, and user IDs.
2. The text is split into smaller chunks using `RecursiveCharacterTextSplitter`.
3. Each chunk is converted into a vector embedding using Sentence Transformers.
4. The embeddings and their associated text and metadata are stored in Qdrant.

**Chunking configuration:**
- Chunk size: 256 tokens.
- Chunk overlap: 50 tokens.
- Embedding dimensions: 384.

The overlap helps preserve context between neighboring chunks.

### 2. Context Retrieval

When a student requests an AI-powered feature:

1. The service receives the request through gRPC.
2. It searches the indexed lecture content for relevant context.
3. Retrieved text is supplied to the language model as part of the prompt.
4. The model generates a response grounded in the retrieved lecture material.
5. The service returns the result through gRPC.

Depending on the operation, the service retrieves context for question generation, essay grading, concept explanation, or personalized revision.

### 3. Vector Storage

Qdrant stores the lecture chunks in a collection named `lecture_chunks`.

Each stored point includes:
- The vector embedding.
- The original text chunk.
- `lecture_id`.
- `course_id`.
- `user_id`.
- `chunk_index`.

The collection uses **cosine similarity** as its configured vector distance metric. Metadata indexes are created for lecture, course, and user IDs.

## 📂 Project Structure

```text
ai-service/
│
├── db/
│   └── vector_store.py
│
├── generation/
│   ├── ai_client.py
│   ├── eplain_text.py
│   ├── generate_summary.py
│   └── prombtBuilder.py
│
├── grpc_server/
│   ├── generate_exam.py
│   ├── generate_explain_text.py
│   ├── grade_answer_handle.py
│   ├── index_lecture.py
│   └── pre_exam_summary.py
│
├── protos/
│   ├── examgen.proto
│   ├── examgen_pb2.py
│   └── examgen_pb2_grpc.py
│
├── Services/
│   ├── chunker.py
│   ├── embedder.py
│   └── retrieval.py
│
├── docker-compose.yml
├── requirement.txt
├── server.py
└── test.py
```

### Main Components

| Component | Responsibility |
|---|---|
| `server.py` | Initializes and runs the gRPC server. |
| `protos/examgen.proto` | Defines the gRPC service contract and message schemas. |
| `Services/chunker.py` | Splits lecture text into overlapping chunks. |
| `Services/embedder.py` | Generates vector embeddings for text chunks. |
| `Services/retrieval.py` | Retrieves lecture content and prepares context for AI operations. |
| `db/vector_store.py` | Manages the Qdrant connection, collection, and stored vectors. |
| `generation/ai_client.py` | Generates exam questions and grades essay answers using Groq. |
| `generation/prombtBuilder.py` | Builds prompts for exam generation and essay grading. |
| `generation/eplain_text.py` | Generates explanations for selected concepts. |
| `generation/generate_summary.py` | Generates focused revision notes for weak topics. |
| `grpc_server/` | Contains the request handlers for the service's AI operations. |

## ⚙️ Getting Started

### Prerequisites

Make sure you have the following installed:

- Python.
- Docker and Docker Compose.
- A Groq API key.

### 1. Clone the Repository

```bash
git clone https://github.com/Rawanfx/Revisio-ai.git
cd Revisio-ai
```

Navigate to the AI service directory:

```bash
cd ai-service
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On Linux or macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirement.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `ai-service` directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual API key.

**Security:** Never commit your `.env` file or expose your API key in source code or public repositories.

### 5. Start Qdrant

The project includes a Docker Compose configuration for running Qdrant.

Start the database:

```bash
docker compose up -d
```

The default configuration exposes:

- **6333:** Qdrant HTTP API.
- **6334:** Qdrant gRPC API.

The vector store client in this project connects to Qdrant at `localhost:6333`.

The Docker Compose configuration also defines persistent storage for the database.

### 6. Run the AI Service

From the `ai-service` directory, run:

```bash
python server.py
```

The gRPC server listens on port `50051`.

On startup, the service ensures that the `lecture_chunks` collection exists before accepting requests.

**Default service address:** `localhost:50051`

## 🔌 gRPC API

The service contract is defined in `protos/examgen.proto`.

The available RPC definitions describe the following operations:

| RPC | Description |
|---|---|
| `IndexLecture` | Indexes lecture content for subsequent retrieval. |
| `GenerateExam` | Generates exam questions according to the requested question count, difficulty distribution, and question types. |
| `GradeAnswer` | Grades a student's written answer using the lecture context and grading criteria. |
| `ExplainConcept` | Explains a selected concept using relevant lecture material. |
| `pre_summary` | Generates focused revision notes for topics the student finds difficult. |

### Example: Indexing a Lecture

The `IndexLecture` request contains:

- `lecture_id`
- `course_id`
- `user_id`
- `content`

The service splits the content, generates embeddings, and stores the resulting chunks in Qdrant.

The response indicates whether the operation succeeded and how many chunks were indexed.

### Example: Generating an Exam

The `GenerateExam` request supports:

- A list of lectures and their requested question counts.
- A total question count.
- A difficulty breakdown: easy, medium, and hard.
- A question-type breakdown: MCQ, true/false, and essay.

Generated questions can include options, correct answers, explanations, topics, model answers, and grading criteria, depending on the question type.

### Example: Grading an Essay

The `GradeAnswer` request includes the lecture ID, question text, student answer, maximum score, model answer, and grading criteria.

The service retrieves relevant lecture context and uses the language model to produce a score, feedback, missing points, and a confidence level.

### Example: Explaining a Concept

The `ExplainConcept` request includes a lecture ID, selected text, and question text.

The service retrieves relevant lecture content and generates an expanded explanation, optionally including a real-world example supported by the source material.

## 🧪 Testing

The repository includes a `test.py` script that demonstrates retrieving lecture context:

```bash
python test.py
```

The script uses a sample lecture ID and question. To obtain meaningful results, the corresponding lecture must already be indexed in Qdrant.

## 🔄 Design Principles

### Separation of Concerns

The service separates request handling, text processing, vector storage, retrieval, and AI generation into distinct modules. This makes individual components easier to maintain and extend.

### Context-Aware AI

AI operations use retrieved lecture content to keep generated questions, grading decisions, explanations, and revision notes relevant to the course material.

### Structured AI Outputs

The language model is instructed to return structured results through tool/function calling, allowing the service to parse generated questions and grading results into application-friendly data structures.

### Multilingual Text Processing

The embedding model and prompt instructions support processing and generating content in the same language as the source material, including Arabic and English.

## 🔮 Future Improvements

Potential areas for further development include:

- Adding automated tests for indexing, retrieval, and AI generation.
- Improving error handling and request validation.
- Adding authentication and secure service communication.
- Implementing image-based answer grading.
- Adding monitoring, logging, and performance metrics.
- Improving retrieval quality and evaluation.
- Adding configurable model and embedding settings.

## 👩‍💻 Part of Revisio AI

This service provides the AI capabilities behind Revisio AI, connecting educational content with retrieval-based AI generation to support exam practice, answer evaluation, concept understanding, and personalized revision.

---

**Built with Python, gRPC, Qdrant, Sentence Transformers, and Groq.**
