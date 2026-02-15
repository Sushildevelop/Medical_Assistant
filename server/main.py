from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware
# from routes.upload_pdfs import router as upload_router
# from routes.ask_question import router as ask_router

app = FastAPI(title="Medical Assistant API", description="API for Medical Assistant Application", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=["*"]
)


#Middleware exception handlers
app.middleware("http")(catch_exception_middleware)


# #routers
# # 1. Upload PDFs
# app.include_router(upload_router)
# # 2. Ask Question
# app.include_router(ask_router)