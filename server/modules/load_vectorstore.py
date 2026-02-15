import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone,ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT ="us-east-1"
PINECONE_INDEX_NAME = "medicalbot-index"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

UPLOAD_DIR = Path("uploaded_docs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

#Initialize Pinecone Instance
pc=Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
spec=ServerlessSpec(
    cloud="aws",
    region=PINECONE_ENVIRONMENT,
)

existing_indexex=[i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexex:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768, 
        metric="cosine", 
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        print("Waiting for Pinecone index to be ready...")
        time.sleep(5)
        
index=pc.Index(PINECONE_INDEX_NAME)

#Load , split , embed and upsert documents 

def load_vectorstore(uploaded_files):
    # embed_model=GoogleGenerativeAIEmbeddings(
    #     model="models/text-embedding-004",
    #     google_api_key=GOOGLE_API_KEY
    # )
    embed_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    file_paths=[]
    
    # 1. Upload
    for file in uploaded_files:
        file_path=Path(UPLOAD_DIR) / file.filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(file_path))
        
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(documents)
        if len(chunks) == 0:
            print(f"No chunks created for {file_path}, skipping...")
            continue

        texts = [chunk.page_content for chunk in chunks]

        # Clean metadata (make it JSON-serializable)
        metadata = []
        for chunk in chunks:
            clean = {}
            for k, v in chunk.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    clean[k] = v
                else:
                    clean[k] = str(v)
            metadata.append(clean)

        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        # 3. Embed
        print("Embedding Chunks")
        raw_embeddings = embed_model.embed_documents(texts)

        # Force embeddings to pure Python floats
        embedding = [list(map(float, vec)) for vec in raw_embeddings]

        # 4. Build vectors
        vectors = list(zip(ids, embedding, metadata))

        # 5. Upsert (batching for safety)
        print("Upserting to Pinecone")
        batch_size = 100

        with tqdm(total=len(vectors), desc="Upserting") as progress:
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i+batch_size]
                index.upsert(vectors=batch)
                progress.update(len(batch))

        print(f"Upload complete for {file_path}")

        
    # # 2. Load and Split
    # for file_path in file_paths:
    #     loader=PyPDFLoader(file_path)
        
    #     documents=loader.load()
        
    #     splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    #     chunks=splitter.split_documents(documents)
        
    #     texts=[chunk.page_content for chunk in chunks]
        
    #     metadata=[chunk.metadata for chunk in chunks]
        
    #     ids=[f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]
        
    #     # 3 .Embed
    #     print(f"Embedding Chunks")
    #     embedding=embed_model.embed_documents(texts)
        
    #     #4. Upsert
    #     print(f"Upserting to Pinecone")
    #     with tqdm(total=len(embedding), desc="Upserting") as progress:
    #         index.upsert(vectors=list(zip(ids,embedding,metadata)))
    #         progress.update(len(embedding))
            
    #     print(f"Upload complete for {file_path}")
        
    




