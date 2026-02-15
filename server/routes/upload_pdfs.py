from fastapi import APIRouter, File, UploadFile
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger

router=APIRouter()

@router.post("/upload_pdfs/")
async def upload_pdfs(
    files:List[UploadFile]=File(...)
):
    try:
        logger.debug(f"Received files for upload.")
        file_paths=load_vectorstore(files)
        logger.debug(f"Successfully processed files: {file_paths}")
        return JSONResponse(content={"message": f"Successfully uploaded and processed files."})
    
    except Exception as e:
        logger.error(f"Error in upload_pdfs: {str(e)}")
        return JSONResponse(content={"error": "An error occurred while processing the files."}, status_code=500)

