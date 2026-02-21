# MedicalBot

MedicalBot is an AI-powered medical assistant chatbot that enables users to upload medical documents (PDFs) and interact with an intelligent system to ask questions and receive responses based on the uploaded content. It leverages Large Language Models (LLMs) and vector stores for efficient document processing and query handling.

## Features

- **Document Upload**: Upload PDF documents containing medical information.
- **Intelligent Querying**: Ask questions about the uploaded documents and get accurate, context-aware responses.
- **Chat Interface**: User-friendly web-based chat UI for seamless interaction.
- **Vector Store Integration**: Efficient storage and retrieval of document embeddings for fast querying.
- **Modular Architecture**: Separate client and server components for scalability.
- **PDF Processing**: Advanced PDF parsing and text extraction capabilities.
- **History Management**: Download chat history for record-keeping.

## Technologies

- **Large Language Model (LLM)**: Groq's Llama 3.1 8B Instant - A fast and efficient language model for generating responses.
- **Vector Database**: Pinecone - A cloud-based vector database for storing and retrieving document embeddings.
- **Embeddings**: Google Generative AI Embeddings or HuggingFace Sentence Transformers - Used to convert text into vector representations for semantic search.
- **Framework**: LangChain - For building and integrating LLM applications with retrieval-augmented generation (RAG).
- **Backend**: FastAPI - A modern, fast web framework for building APIs.
- **Frontend**: Streamlit - For creating the interactive web interface.

## Project Structure

```
MedicalBot/
├── main.py                 # Main entry point
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
├── client/                 # Frontend application
│   ├── app.py              # Client application entry point
│   ├── config.py           # Client configuration
│   ├── requirements.txt    # Client dependencies
│   ├── components/         # UI components
│   │   ├── chatUI.py       # Chat interface component
│   │   ├── history_download.py  # History download component
│   │   └── upload.py       # File upload component
│   └── utils/
│       └── api.py          # API utilities
├── server/                 # Backend server
│   ├── main.py             # Server application entry point
│   ├── requirements.txt    # Server dependencies
│   ├── test.py             # Server tests
│   ├── logger.py           # Logging configuration
│   ├── middlewares/        # Server middlewares
│   │   └── exception_handlers.py  # Exception handling
│   ├── modules/            # Core business logic
│   │   ├── llm.py          # Language model integration
│   │   ├── load_vectorstore.py  # Vector store management
│   │   ├── pdf_handlers.py # PDF processing
│   │   └── query_handlers.py   # Query processing
│   ├── routes/             # API routes
│   │   ├── ask_question.py # Question answering endpoint
│   │   └── upload_pdfs.py  # PDF upload endpoint
│   └── uploaded_docs/      # Directory for uploaded documents
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd MedicalBot
   ```

2. **Install dependencies**:
   - For the entire project (using pyproject.toml):
     ```bash
     pip install -e .
     ```
   - Or install client and server dependencies separately:

     ```bash
     # Client dependencies
     cd client
     pip install -r requirements.txt

     # Server dependencies
     cd ../server
     pip install -r requirements.txt
     ```

3. **Configure the application**:
   - Update configuration files (`client/config.py`, `server/config.py` if applicable) with necessary API keys, database connections, etc.
   - Ensure you have access to required LLM services (e.g., OpenAI API key for GPT models).

## Usage

### Running the Server

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Start the server:
   ```bash
   python main.py
   ```
   The server will start on the configured port (default: 8000).

### Running the Client

1. Navigate to the client directory:

   ```bash
   cd client
   ```

2. Start the client application:
   ```bash
   python app.py
   ```
   The client will be accessible via your web browser at the configured URL (default: http://localhost:3000).

### Using the Application

1. Open the client in your web browser.
2. Upload PDF documents containing medical information.
3. Start asking questions in the chat interface.
4. Download chat history if needed.

## API Endpoints

- `POST /upload-pdfs`: Upload PDF documents
- `POST /ask-question`: Submit questions and receive responses

## Development

### Running Tests

```bash
cd server
python test.py
```

### Adding New Features

- Client components: Add to `client/components/`
- Server modules: Add to `server/modules/`
- API routes: Add to `server/routes/`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.
