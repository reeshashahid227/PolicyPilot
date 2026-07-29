# 🏛️ PolicyPilot

## AI-Powered Policy Assistant using Retrieval-Augmented Generation (RAG)

PolicyPilot is an AI-powered policy assistant that answers questions about company policies using a **Retrieval-Augmented Generation (RAG)** pipeline.

Instead of asking an LLM to answer from its general knowledge, PolicyPilot first retrieves relevant information from the policy documents and then uses that retrieved context to generate a grounded response.

The application also displays the **sources used to produce the answer**, making the response more transparent and easier to verify.

---

## 🚀 Live Demo

### 🌐 Streamlit Application

**https://policypilot-jifgmb3kctvb6e9bzxvszi.streamlit.app/**

---

## ✨ Features

- 📄 Policy document ingestion (Markdown-based handbook)
- 🧹 Text cleaning and preprocessing
- ✂️ Document chunking
- 🧠 Semantic embeddings
- 🔎 FAISS-based similarity retrieval
- 🤖 Groq-powered LLM generation
- 📚 Source/citation display
- 🛡️ Grounded responses to reduce hallucinations
- 💬 Interactive Streamlit chat interface
- 🧩 Modular `PolicyEngine`
- ⚡ FastAPI API layer
- ☁️ Public Streamlit deployment
- 🔐 Environment-variable based API key management

---

# 🧠 What Problem Does PolicyPilot Solve?

Company policy documents can be long and difficult to search manually.

An employee may ask:

- What is the remote work policy?
- How many annual leave days are available?
- What is the sick leave policy?
- What benefits are available?

PolicyPilot lets the user ask these questions naturally and retrieves relevant information from the available policy documents before generating the answer.

---

# 🔄 RAG Pipeline

```text
                    Policy Documents (Markdown)
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
                Sentence Transformers
                           │
                           ▼
                   FAISS Vector Index
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
                Answer + Source Citations
                           │
                           ▼
                    Streamlit Interface
```

---

# 🏗️ Project Structure

```text
PolicyPilot/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── data/
│   ├── raw/
│   │   └── handbook-master/
│   │       ├── Benefits and Perks/
│   │       ├── Clef Values.md
│   │       ├── Mission Statement.md
│   │       ├── Policy Changes.md
│   │       └── README.md
│   │
│   └── processed/
│       ├── chunks.json
│       └── policy.index
│
├── scripts/
│   └── ...
│
└── src/
    ├── __init__.py
    │
    ├── api/
    │   ├── __init__.py
    │   ├── main.py
    │   └── schemas.py
    │
    ├── core/
    │   ├── __init__.py
    │   └── policy_engine.py
    │
    ├── ingestion/
    │   ├── __init__.py
    │   ├── loader.py
    │   ├── cleaner.py
    │   ├── chunker.py
    │   └── metadata.py
    │
    ├── embeddings/
    │   ├── __init__.py
    │   └── embedder.py
    │
    ├── retrieval/
    │   ├── __init__.py
    │   └── retriever.py
    │
    └── generation/
        ├── __init__.py
        ├── llm_generator.py
        └── citations.py
```

---

# 🧩 Main Components

## 1. Document Ingestion

The ingestion layer prepares the policy documents (Markdown files) for the RAG system.

```text
Raw Markdown Documents
     ↓
Loader
     ↓
Cleaner
     ↓
Metadata Extraction
     ↓
Chunker
     ↓
Processed Chunks
```

The `loader` module reads the Markdown-based policy handbook, and the `cleaner` module normalizes the text before chunking, ensuring consistent input for the embedding stage.

---

## 2. Embeddings

The text chunks are converted into semantic vector representations using a Sentence Transformer embedding model.

This allows the system to compare the meaning of a user's question with the meaning of policy chunks.

```text
Policy Chunk
     ↓
Embedding Model
     ↓
Vector Representation
```

---

## 3. FAISS Retrieval

FAISS is used for efficient similarity search.

When the user asks a question, the question is embedded and compared with the indexed policy vectors.

```text
User Question
     ↓
Question Embedding
     ↓
FAISS Similarity Search
     ↓
Top Relevant Policy Chunks
```

---

# 🧠 PolicyEngine

`PolicyEngine` is the core orchestration layer of PolicyPilot.

It connects the major RAG components instead of placing all of the application logic directly inside the Streamlit interface.

```text
                 PolicyEngine
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      Retriever              LLMGenerator
          │                       │
          ▼                       ▼
   FAISS + Embeddings           Groq
          │                       │
          └───────────┬───────────┘
                      ▼
               Answer + Sources
```

This separation makes the project easier to maintain and allows the same core logic to be used by different interfaces.

---

# 🤖 Answer Generation

The `LLMGenerator` uses the retrieved policy chunks as context for the Groq LLM.

The generation logic follows strict grounding rules:

1. Use only the retrieved policy context.
2. Do not use outside knowledge.
3. Do not invent company policy.
4. Do not make unsupported assumptions.
5. If the retrieved context does not contain the answer, clearly say that the information was not found.

This helps reduce hallucinated policy answers.

---

# 📚 Citations

After retrieval and answer generation, PolicyPilot formats the retrieved policy information into source references.

The Streamlit UI displays these sources underneath the generated answer.

```text
Question
   ↓
Retrieve relevant chunks
   ↓
Generate grounded answer
   ↓
Format citations
   ↓
Answer + Sources
```

---

# 🎨 Streamlit Interface

The Streamlit application provides the user-facing chat experience.

The interface includes:

- 🏛️ PolicyPilot branding
- 💬 Chat-based question answering
- 💡 Example policy questions
- 🗑️ Conversation clearing
- 🔎 Retrieval status
- 📚 Source display
- 📱 Responsive Streamlit layout

The live application is available here:

**https://policypilot-jifgmb3kctvb6e9bzxvszi.streamlit.app/**

---

# ⚡ FastAPI API

PolicyPilot also contains a FastAPI layer that exposes the RAG pipeline through API endpoints.

Main endpoints:

```text
GET  /
GET  /health
POST /ask
```

### Example request

```json
{
  "question": "What is the remote work policy?"
}
```

### Example response

```json
{
  "answer": "Generated answer based on retrieved policy context.",
  "sources": []
}
```

The FastAPI layer separates the backend RAG logic from the Streamlit presentation layer and makes the project easier to integrate with other clients in the future.

---

# 🔗 Why FastAPI?

Streamlit is used for the **interactive user interface**, while FastAPI provides a **backend/API layer**.

```text
                  PolicyPilot
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      Streamlit               FastAPI
        UI                     API
          │                       │
          └───────────┬───────────┘
                      ▼
                 PolicyEngine
                      │
             ┌────────┴────────┐
             ▼                 ▼
         Retriever        LLMGenerator
             │                 │
            FAISS            Groq
```

This architecture demonstrates how the same RAG core can support a web UI as well as an API interface.

---

# 🛠️ Technology Stack

| Technology            | Purpose                          |
| ---------------------- | --------------------------------- |
| Python                 | Core programming language         |
| Streamlit              | Interactive web interface         |
| FastAPI                | REST API layer                    |
| FAISS                  | Vector similarity search          |
| Sentence Transformers  | Semantic embeddings               |
| Groq                   | LLM-based answer generation       |
| Pathlib                | File and directory path handling  |
| NumPy                  | Numerical operations               |
| python-dotenv          | Environment variable management   |

---

# 📁 Path Management

`pathlib.Path` is used for file and directory path handling where required.

Example:

```python
from pathlib import Path
```

Pathlib provides cleaner and more cross-platform path management than manually constructing filesystem paths.

---

# 💻 Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/reeshashahid227/PolicyPilot.git
cd PolicyPilot
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Add environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Do not commit `.env` to GitHub.

---

# ▶️ Run Streamlit

From the project root:

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

---

# ⚡ Run FastAPI

From the project root:

```bash
python -m uvicorn src.api.main:app --reload
```

Local API:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Test FastAPI

Open:

```text
http://127.0.0.1:8000/docs
```

Then:

1. Open `POST /ask`
2. Click **Try it out**
3. Enter a question
4. Click **Execute**
5. Review the answer and sources

Example:

```json
{
  "question": "What is the sick leave policy?"
}
```

---

# 🔐 Environment Variables

Required:

```env
GROQ_API_KEY=your_groq_api_key
```

Recommended `.gitignore` entries:

```text
.env
venv/
__pycache__/
*.pyc
```

Never expose API keys in source code or public repositories.

---

# 📊 Project Highlights

### 🔎 Complete RAG Pipeline

PolicyPilot demonstrates the complete flow from raw policy documents to retrieved context and LLM-generated answers.

### 🧠 Semantic Retrieval

The system retrieves information based on semantic similarity rather than relying only on exact keyword matches.

### ⚡ Vector Search

FAISS is used to efficiently search the embedding index.

### 📚 Grounded Answers

The LLM receives retrieved policy context and is instructed not to invent unsupported policy information.

### 🔗 Source Transparency

Relevant source information is displayed alongside answers.

### 🧩 Modular Architecture

The project separates ingestion, embeddings, retrieval, generation, core orchestration, API, and UI responsibilities.

---

# 🚀 Deployment

The public Streamlit interface is deployed here:

### 🌐 Live Demo

**https://policypilot-jifgmb3kctvb6e9bzxvszi.streamlit.app/**

The project also contains a FastAPI backend layer for exposing the RAG pipeline as an API when required.

---

# 📈 Future Improvements

- 🔐 Authentication and role-based access
- 📄 Support for additional document formats (PDF, DOCX)
- 🗂️ Multiple policy collections
- 🔎 Hybrid keyword + semantic retrieval
- 📊 Retrieval evaluation metrics
- 🧪 Automated RAG evaluation
- 💾 Persistent conversation history
- ⚡ Streaming LLM responses
- 🏢 Organization-specific policy workspaces
- 📌 Enhanced document navigation and citations

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Document ingestion and preprocessing
- Embeddings
- Vector databases
- Semantic search
- LLM integration
- Prompt engineering
- PolicyEngine architecture
- FastAPI
- Streamlit
- Pathlib
- Modular Python architecture
- Environment variable management
- Git and GitHub
- Cloud deployment