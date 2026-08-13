from transformers import AutoTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter
model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer,
    chunk_size=256,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", "!", "?", " ", ""]
)

def create_chunk(text:str)->list[str]:
    return text_splitter.split_text(text)
