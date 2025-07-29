> **Note:** This README is currently AI-generated and undergoing review.


# MetaRagTool 🚀



**MetaRagTool** is a flexible Python framework designed to simplify the creation and evaluation of Retrieval-Augmented Generation (RAG) systems. Whether you're building a simple question-answering bot or experimenting with advanced retrieval techniques, MetaRagTool provides the building blocks you need.

[![PyPI version](https://badge.fury.io/py/MetaRagTool.svg)](https://badge.fury.io/py/MetaRagTool) <!-- Placeholder - update if you publish -->
<!-- Add other badges like License, Build Status etc. if applicable -->

## ✨ Key Features

*   **Easy RAG Setup:** Quickly configure and run RAG pipelines.
*   **Flexible Components:** Integrates with popular libraries like `sentence-transformers` and `google-generativeai`.
*   **Multiple Interaction Modes:**
    *   Retrieve relevant documents (`retrieve`).
    *   Ask questions directly using retrieved context (`ask`).
    *   Let the LLM decide when to retrieve information using tools (`ask(useTool=True)`).
*   **Document Handling:** Load and process text data, including direct PDF reading.
*   **Configurable Chunking:** Choose from various strategies (sentence splitting, merging, paragraphs, recursive).
*   **Advanced Retrieval Options:** Experiment with techniques like adding neighbor chunks or using parent paragraph context.
*   **Built-in LLMs:** Supports Google Gemini out-of-the-box (and potentially others like OpenAI based on imports).
*   **Evaluation Tools:** Includes utilities for evaluating retrieval performance (see `MetaRagTool.Evaluations`).
*   **Demo UI:** Comes with Gradio apps for interactive testing (see `MetaRagTool.Apps`).

## ⚙️ Installation

Get started by installing the package using pip:

```bash
pip install MetaRagTool
```

*(Note: Depending on the specific encoders or LLMs you use, you might need additional dependencies like `sentence-transformers`, `google-generativeai`, `PyPDF2`, `faiss-cpu` or `faiss-gpu` etc. The core installation handles the framework itself.)*

## ⚡ Quick Start: Your First RAG Query

This example shows the absolute minimum to get a RAG system running and answer a question.

```python
import MetaRagTool
from MetaRagTool import MetaRAG, Gemini, SentenceTransformerEncoder

# --- Configuration ---
# 1. Set API Keys (replace 'YOUR_API_KEY' with your actual key)
# You can also set keys globally using MetaRagTool.Constants.SetTokens(t_gemini='YOUR_API_KEY')
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" # Required for Gemini LLM

# 2. Choose an Encoder Model
# Using a local path or a Hugging Face model name
encoder = SentenceTransformerEncoder('sentence-transformers/LaBSE')
# or from a local path: encoder = SentenceTransformerEncoder('/path/to/your/LaBSE/model')

# 3. Choose an LLM
llm = Gemini(api_key=GEMINI_API_KEY)

# --- Setup RAG ---
# 4. Initialize MetaRAG
rag = MetaRAG(encoder_model=encoder, llm=llm)

# 5. Add Your Data (Corpus)
# This should be a list of strings, where each string is a HUGE document or a significant text block.
contexts = [
    "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
    "It is named after the engineer Gustave Eiffel, whose company designed and built the tower.",
    "Constructed from 1887 to 1889 as the entrance arch for the 1889 World's Fair.",
    "The tower is 330 metres (1,083 ft) tall, about the same height as an 81-storey building.",
    "The tower has three levels for visitors, with restaurants on the first and second levels."
]
rag.add_corpus(contexts)

# --- Ask a Question ---
# 6. Perform RAG Query
query = "How tall is the Eiffel Tower?"

response = rag.ask(query) # This retrieves relevant chunks and asks the LLM

# Alternatively, you can retrieve chunks separately without any LLM processing:
# retrieved_chunks = rag.retrieve(query, top_k=10) # Get top 3 relevant chunks


print(f"\nAnswer:\n{response}")
```

## 📖 Usage Examples

### 1. Initialization

Import the necessary classes and initialize the core components: Encoder, LLM, and the `MetaRAG` orchestrator.

```python
import MetaRagTool
from MetaRagTool import MetaRAG, Gemini, SentenceTransformerEncoder
from MetaRagTool.Utils import read_pdf # Helper for reading PDFs

# --- API Key Setup ---
# Best practice: Use environment variables or a secure method.
# Or set globally once:
# MetaRagTool.Constants.SetTokens(t_gemini="YOUR_GEMINI_API_KEY")
# Or pass directly during LLM initialization:
llm = Gemini(api_key="YOUR_GEMINI_API_KEY")

# --- Encoder Setup ---
# Choose any Sentence Transformer model (Hugging Face name or local path)
encoder = SentenceTransformerEncoder('sentence-transformers/LaBSE')

# --- RAG Orchestrator ---
rag = MetaRAG(
    encoder_model=encoder,
    llm=llm,
    # Optional: Configure chunking, retrieval methods here
    # splitting_method=MetaRagTool.RAG.ChunkingMethod.SENTENCE_MERGER,
    # chunk_size=100
)
print("MetaRAG initialized.")
```

### 2. Adding Data

You can add data from a list of strings or directly from PDF files.

```python
# --- Add from Text List ---
text_contexts = [
    "Document 1 text...",
    "Document 2 text...",
]
rag.add_corpus(text_contexts)
print("Text corpus added.")

# --- Add from PDF Files ---
# Make sure you have PyPDF2 installed: pip install PyPDF2
pdf_files = ["./my_document1.pdf", "./my_document2.pdf"]
pdf_contexts = []
for pdf_path in pdf_files:
    try:
        pdf_contexts.append(read_pdf(pdf_path))
        print(f"Read content from {pdf_path}")
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

if pdf_contexts:
    rag.add_corpus(pdf_contexts)
    print("PDF corpus added.")

# The `add_corpus` method handles chunking and embedding automatically.
```

### 3. Retrieving Relevant Chunks (`rag.retrieve`)

If you only want the relevant text chunks without asking the LLM to synthesize an answer:

```python
query = "What was Gustave Eiffel's role?"
top_k = 5 # Number of chunks to retrieve

retrieved_chunks = rag.retrieve(query, top_k=top_k)

print(f"Query: {query}")
print(f"\nRetrieved Chunks (Top {top_k}):")
for i, chunk in enumerate(retrieved_chunks):
    print(f"--- Chunk {i+1} ---")
    print(chunk)
    print("-" * 15)
```

### 4. Asking Questions with Context (`rag.ask`)

This is the standard RAG approach. It retrieves relevant chunks and then passes them along with your query to the LLM to generate a concise answer.

```python
query = "Where is the Eiffel Tower located?"
top_k_for_llm = 10 # How many chunks to provide as context

answer = rag.ask(query, top_k=top_k_for_llm)

print(f"Query: {query}")
print(f"\nGenerated Answer:\n{answer}")
```

### 5. Tool-Based RAG (`rag.ask(useTool=True)`)

This approach gives the LLM access to the `retrieve` function as a tool. The LLM decides *if* and *when* to call the retrieval tool based on the query. This can be useful for conversational agents or more complex queries where the LLM might need to refine its search.

```python
query = "Tell me about the history and height of the Eiffel Tower."

# Let the LLM use the retrieval tool as needed
tool_answer = rag.ask(query, useTool=True)

print(f"Query: {query}")
print(f"\nTool-Based Answer:\n{tool_answer}")

# Note: The LLM might make one or more calls to the retrieval tool behind the scenes.
# You can inspect rag.llm.messages_history (if history is enabled) to see the interaction.
```

## 🧩 Core Components

*   **`MetaRAG`:** The main class that orchestrates the RAG pipeline, managing data ingestion, chunking, embedding, retrieval, and interaction with the LLM.
*   **Encoders (`MetaRagTool.Encoders`)**: Classes responsible for converting text into vector embeddings.
    *   `SentenceTransformerEncoder`: Uses models from the `sentence-transformers` library. Other encoders might be available.
*   **LLMs (`MetaRagTool.LLM`)**: Classes for interacting with Large Language Models.
    *   `Gemini`: Interfaces with Google's Gemini models.
    *   `JudgeLLM`: A specialized LLM for evaluating answer quality (used in evaluations). Potentially `OpenaiGpt` based on imports.
*   **Chunking Methods (`MetaRagTool.RAG.ChunkingMethod`)**: An Enum defining different strategies for splitting documents (e.g., `SENTENCE_MERGER`, `PARAGRAPH`, `RECURSIVE`).
*   **Utilities (`MetaRagTool.Utils`)**: Helper functions for tasks like loading data (`DataLoader`), reading PDFs (`MyUtils.read_pdf`), etc.
*   **Evaluations (`MetaRagTool.Evaluations`)**: Tools and scripts for assessing the performance of your RAG setup, particularly retrieval effectiveness.
*   **Apps (`MetaRagTool.Apps`)**: Gradio-based demonstration applications.

## 🔧 Configuration & Customization

You can customize the `MetaRAG` behavior during initialization:

```python
from MetaRagTool.RAG import ChunkingMethod

rag = MetaRAG(
    encoder_model=encoder,
    llm=llm,

    # --- Chunking ---
    splitting_method=ChunkingMethod.SENTENCE_MERGER, # Strategy
    chunk_size=120,           # Target token count per chunk
    chunk_overlap=10,         # Token overlap between chunks
    max_sentence_len=100,     # Max tokens before splitting a sentence

    # --- Advanced Retrieval ---
    add_neighbor_chunks_smart=True, # Intelligently add adjacent chunks if relevant
    replace_retrieved_chunks_with_parent_paragraph=True, # Retrieve the whole paragraph instead of just the chunk
    use_neighbor_embeddings=False, # Factor in neighbor embeddings (experimental)
    use_parentParagraph_embeddings=False, # Factor in paragraph embeddings (experimental)

    # --- Other ---
    normalize_text=True,      # Apply text normalization (e.g., using hazm)
    # ... other parameters available
)
```

Refer to the `MetaRAG` class definition (`MetaRagTool/RAG/MetaRAG.py`) for all available parameters.

## 📈 Evaluation

MetaRagTool includes an evaluation framework (see `MetaRagTool.Evaluations` and `Scripts/Evaluations`) to test different configurations, encoders, and retrieval strategies. This often involves using datasets like WikiFaQA and measuring retrieval accuracy (e.g., did the correct context get retrieved?) or using an LLM Judge for end-to-end quality assessment.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs, feature requests, or improvements.

```