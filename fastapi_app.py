
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

# Assumes these are already loaded in memory:
# text_model
# clip_model, clip_processor
# collection
# embed_text(text) and embed_image(img) functions

app = FastAPI(title="Multimodal RAG API")

# Mount images folder
IMAGE_DIR = "/content/mkdocs_images_extracted"  # or "mkdocs_images_extracted"
app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

@app.get("/")
def root():
    return {"message": "Multimodal RAG API is running!"}

@app.post("/search")
async def search(query: str = Form(...), n_results: int = Form(5)):
    if query.strip() == "":
        return JSONResponse(status_code=400, content={"error": "Query is empty"})

    # Embed the text query
    emb = embed_text(query)

    # Query the multimodal collection
    results = collection.query(query_embeddings=[emb], n_results=n_results)

    response = {"query": query, "results": []}
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for d, m in zip(docs, metas):
        item = {"source": m.get("source", "unknown")}

        # Check if it's an image
        if d.lower().endswith((".png", ".jpg", ".jpeg")) and os.path.exists(d):
            filename = os.path.basename(d)
            item["type"] = "image"
            item["path"] = f"/images/{filename}"  # Serve via FastAPI static route
        else:
            item["type"] = "text"
            item["text"] = d

        response["results"].append(item)

    return response
