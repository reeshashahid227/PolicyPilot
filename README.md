# 🏛️ PolicyPilot

### AI-Powered Policy Assistant using Retrieval-Augmented Generation (RAG)

PolicyPilot is an AI-powered policy assistant that allows users to ask questions about company policies and receive **document-grounded answers with relevant source citations**.

Instead of relying only on an LLM's internal knowledge, PolicyPilot retrieves relevant information from policy documents first and then provides that context to the language model for answer generation.

---

## 🚀 Live Demo

**Streamlit App:**  
https://policypilot-jifgmb3kctvb6e9bzxvszi.streamlit.app/

---

## ✨ Key Features

- 📄 Policy document ingestion and preprocessing
- 🧹 Text cleaning and normalization
- ✂️ Document chunking for efficient retrieval
- 🧠 Semantic embeddings using Sentence Transformers
- 🔎 Similarity search using FAISS
- 🤖 Grounded answer generation using Groq LLM
- 📚 Source/citation display for retrieved policy information
- 🛡️ RAG-based protection against unsupported answers
- 💬 Interactive Streamlit chat interface
- ⚡ PolicyEngine for connecting retrieval and generation
- 🔌 FastAPI REST API for exposing the RAG pipeline
- ☁️ Streamlit deployment for public access

---

## 🧠 What Problem Does PolicyPilot Solve?

Employees often need quick answers to questions such as:

- What is the remote work policy?
- How many annual leave days are available?
- What is the sick leave policy?
- What employee benefits are available?

Searching through long policy documents manually can be slow and frustrating.

PolicyPilot provides a conversational interface where users can ask questions naturally and receive answers grounded in the available policy documents.

---

# 🔄 RAG Pipeline

```text
                    Policy Documents
                           │
                           ▼
                  Document Ingestion
                           │
                           ▼
                   Text Cleaning
                           │
                           ▼
                    Text Chunking
                           │
                           ▼
                  Embedding Model
                           │
                           ▼
                    FAISS Index
                           │
                           │
                    User Question
                           │
                           ▼
                      Retriever
                           │
                           ▼
                Relevant Policy Chunks
                           │
                           ▼
                     PolicyEngine
                           │
                           ▼
                       Groq LLM
                           │
                           ▼
                Grounded Answer + Sources
                           │
                           ▼
                     Streamlit UI
```

---

# 🏗️ Architecture

PolicyPilot is organized into separate layers so that each component has a clear responsibility.

```text
PolicyPilot/
│
├── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── chunks.json
│       └── policy.index
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── schemas.py
│   │
│   ├── core/
│   │   └── policy_engine.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── generation/
│   │   ├── llm_generator.py
│   │   └── citations.py
│   │
│   └── ingestion/
│       ├── loader.py
│       ├── cleaner.py
│       ├── chunker.py
│       └── metadata.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| FastAPI | REST API layer |
| FAISS | Vector similarity search |
| Sentence Transformers | Semantic embeddings |
| Groq | LLM-based answer generation |
| PyMuPDF | PDF/document processing |
| NumPy | Numerical operations |
| python-dotenv | Environment variable management |

---

# 🔍 How Retrieval Works

When a user submits a question:

1. The question is converted into an embedding.
2. FAISS searches the vector index for semantically similar chunks.
3. The most relevant policy chunks are selected.
4. PolicyEngine passes the retrieved context to the LLM.
5. The LLM generates an answer using only the retrieved policy context.
6. The application displays the answer and its sources.

This approach helps reduce hallucinations because the model is explicitly instructed not to invent policy information.

---

# 🛡️ Grounded Generation

PolicyPilot uses strict generation instructions:

- Use only retrieved policy context.
- Do not use outside knowledge.
- Do not invent policy information.
- Do not make assumptions.
- If the answer is not supported by the retrieved documents, clearly state that the information was not found.

This makes the application more suitable for policy-related question answering than a generic chatbot.

---

# 🧩 PolicyEngine

`PolicyEngine` acts as the main orchestration layer of the application.

It connects the major RAG components:

```text
User Question
      │
      ▼
PolicyEngine
      │
      ├── Retriever
      │      └── FAISS + Embeddings
      │
      └── LLMGenerator
             └── Groq
      │
      ▼
Answer + Sources
```

This keeps the Streamlit UI focused on presentation while the core RAG logic remains inside the application architecture.

---

# 🔌 FastAPI Layer

PolicyPilot also includes a FastAPI API layer.

The API exposes the RAG functionality through endpoints such as:

```text
GET  /
GET  /health
POST /ask
```

Example request:

```json
{
  "question": "What is the remote work policy?"
}
```

Example response:

```json
{
  "answer": "The answer generated from the retrieved policy context...",
  "sources": [
    {
      "source": "Remote Work Policy"
    }
  ]
}
```

The FastAPI layer demonstrates how the RAG pipeline can be exposed as a reusable backend service instead of being limited to a Streamlit application.

---

# 💻 Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/reeshashahid227/PolicyPilot.git
cd PolicyPilot
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.env\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your API key to GitHub.

## 5. Run Streamlit

```bash
streamlit run app.py
```

The application will open in your browser.

---

# ⚡ Run FastAPI

From the project root:

```bash
python -m uvicorn src.api.main:app --reload
```

The API will run locally at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Testing the API

You can test the `/ask` endpoint using the FastAPI Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

Then:

1. Open `POST /ask`
2. Click **Try it out**
3. Enter a question
4. Click **Execute**
5. Check the generated answer and sources

---

# 🔐 Environment Variables

The project uses environment variables for secrets.

Required:

```env
GROQ_API_KEY=your_groq_api_key
```

Example `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# 📊 Project Highlights

### Retrieval-Augmented Generation

The project demonstrates a complete RAG workflow rather than sending user questions directly to an LLM.

### Semantic Search

Policy chunks are converted into embeddings so that questions can retrieve semantically related information even when the wording differs.

### Vector Database

FAISS provides efficient similarity search over the generated embeddings.

### Source Grounding

Retrieved sources are returned with the answer so users can understand where the response came from.

### Modular Architecture

The project separates ingestion, embeddings, retrieval, generation, API, and UI responsibilities.

---

# 🚀 Deployment

The Streamlit interface is publicly deployed and available here:

**Live Application:**  
https://policypilot-jifgmb3kctvb6e9bzxvszi.streamlit.app/

The project is structured so the RAG logic can also be exposed through FastAPI as a backend service when required.

---

# 📈 Future Improvements

Possible future improvements include:

- 🔐 Authentication and role-based access
- 📄 Support for more document formats
- 🗂️ Multiple policy collections
- 🔎 Hybrid keyword + semantic retrieval
- 📊 Retrieval evaluation metrics
- 🧪 Automated RAG evaluation
- 💾 Conversation persistence
- ⚡ Streaming LLM responses
- 🏢 Organization-specific policy workspaces
- 📌 Better citation metadata and document navigation

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation
- Embeddings
- Vector databases
- Semantic search
- LLM integration
- Prompt engineering
- FastAPI
- Streamlit
- Modular Python architecture
- Environment variable management
- Git and GitHub
- Cloud deployment

---


