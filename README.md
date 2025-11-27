# Multimodal RAG System for MkDocs Documentation

This project implements a **Retrieval-Augmented Generation (RAG) system** for [MkDocs](https://github.com/mkdocs/mkdocs), an open-source static site generator for project documentation. The system allows users to query the MkDocs documentation and retrieve answers from the docs, with support for **multimodal queries** (text + images) via embeddings. Done on Google Colab the link is in the end of README .

## Features

- Text retrieval from MkDocs documentation using **Chroma** vector database.
- Embeddings generated with **Sentence-Transformers** (`all-MiniLM-L6-v2`).
- Optional **multimodal search** using **CLIP embeddings** for both text and images.
- Web API via **FastAPI** accessible publicly using **Cloudflared** tunnel.
- Simple **HTML frontend** for querying text and displaying image results.

---

# Install dependencies
pip install sentence-transformers==2.6.1
pip install chromadb==0.5.3
pip install markdown
pip install beautifulsoup4
pip install requests
pip install streamlit
pip install nltk
pip install transformers
pip install Pillow

# Chunking Method

Method: Sentence-based sliding window

Parameters: 5 sentences per chunk, 2-sentence overlap

Reason: Preserves context across chunks while avoiding overly large segments that can dilute embeddings.
pip install fastapi uvicorn

# Chunks Cleaning

Steps:

- Remove Markdown code blocks
- Remove HTML tags
- Collapse whitespace
- Reason: Ensures that chunks contain only meaningful textual content for embeddings.

| Purpose               | Model                                      |
| --------------------- | ------------------------------------------ |
| Text embeddings       | `all-MiniLM-L6-v2` (Sentence-Transformers) |
| Multimodal embeddings | `openai/clip-vit-base-patch32` (CLIP)      |
| LLM for answers       | `tiiuae/falcon-7b-instruct`                |

# Vector Database

- Chroma DB is used to store embeddings.
- Supports persistent storage and efficient similarity search.

Separate collections for:
- Text chunks
- Multimodal embeddings (text + images)

# Sample Query
```bash
query = "How does MkDocs build static sites?"
answer = answer_query_local(query, k=3)
print(answer)
```

- Retrieves top 3 chunks relevant to the query.
- LLM generates a concise answer using the retrieved context.

# Bonus: Multimodal Embeddings

- Extracts images from MkDocs documentation.
- Generates CLIP embeddings for both text and images.
- Enables retrieval of relevant images along with text.
  
# FastAPI Application

- Exposes a /search endpoint for multimodal queries.
- Serves images via a static route.
- Can be exposed publicly using Cloudflared.
 HTML frontend:
- Enter a query in the input box, click Search, and view text answers and images retrieved from the multimodal RAG system.
  
 # Running the app
 - Run the FastApi App code
 - Run the open FastApi and open tunnel using cloudflared code
 - A url will be generated copy it and paste it in this part of index.html  "// Replace this URL with your Cloudflared public URL (no trailing slash) const url = "https://heated-explained-satisfied-ohio.trycloudflare.com"; "
 - now in terminal run python "-m http.server 5500" to run index.html
 - open the browser and search "http://localhost:5500/index.html" to open the app on the browser
 
# Project Structure
  mkdocs-rag/
- mkdocs/                  # Cloned MkDocs repo
-  chromadb/                # Vector DB persistence
- mkdocs_images_extracted/ # Extracted images
- fastapi_app.py           # API backend
- index.html               # Web frontend
- requirements.txt
-  README.md
  
# Colab Link
https://colab.research.google.com/drive/1TV-v0uLPO6FrK5edkXyArq01ewxc0QO1?usp=sharing
