from fastapi import APIRouter, Form
from pydantic import Field
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
from dotenv import load_dotenv
from typing  import List,Optional
from logger import logger
import os

router=APIRouter()

@router.post("/ask/")
async def ask_question(
    question:str=Form(...),
    top_k:int=Form(5)
):
    try:
        logger.debug(f"Received question: {question} with top_k: {top_k}")
        
        # Initialize retriever
        pc=Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index=pc.Index(os.environ["PINECONE_INDEX_NAME"])
        
        # embed_model=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        embed_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        embedded_query=embed_model.embed_query(question)
        
        res=index.query(vector=embedded_query, top_k=top_k, include_metadata=True)
        
        docs=[
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
                
            )for match in res["matches"]
            
        ]
        class SimpleRetriever(BaseRetriever):
            tags:Optional[List[str]] = Field(default_factory=list)
            metadata:Optional[dict]=Field(default_factory=dict)
            def __init__(self,documents:List[Document]):
                super().__init__()
                self._docs=documents
                
              # Sync version (REQUIRED)
            def _get_relevant_documents(self, query: str):
                return self._docs

            # Async version (REQUIRED)
            async def _aget_relevant_documents(self, query: str):
                return self._docs
            
        retriever=SimpleRetriever(docs)
        chain=get_llm_chain(retriever)
        
        result=query_chain(chain,question)
        logger.debug(f"Final response: {result}")
        return result
        
    
    except Exception as e:
        logger.error(f"Error in ask_question: {str(e)}")
        return JSONResponse(content={"error": "An error occurred while processing the question."}, status_code=500
)