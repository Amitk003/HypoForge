import hashlib
from typing import Optional

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")
    EMBED_DIM = 384
except Exception:
    EMBEDDER = None
    EMBED_DIM = 0

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_CLIENT = chromadb.PersistentClient(
        path="chroma_db",
        settings=Settings(anonymized_telemetry=False),
    )
except Exception:
    CHROMA_CLIENT = None


def get_collection(name: str = "papers"):
    if CHROMA_CLIENT is None:
        return None
    try:
        return CHROMA_CLIENT.get_or_create_collection(name=name)
    except Exception:
        return None


def embed_texts(texts: list[str]) -> Optional[list[list[float]]]:
    if EMBEDDER is None:
        return None
    try:
        return EMBEDDER.encode(texts).tolist()
    except Exception:
        return None


def index_papers(papers: list[dict], collection_name: str = "papers") -> int:
    col = get_collection(collection_name)
    if col is None or not papers:
        return 0

    texts = []
    metadatas = []
    ids = []
    for p in papers:
        content = f"{p['title']} {p.get('summary', '')}"
        content_hash = hashlib.md5(content.encode()).hexdigest()
        texts.append(content)
        metadatas.append({"title": p["title"], "source": p.get("source", "arxiv")})
        ids.append(content_hash)

    embeddings = embed_texts(texts)
    if embeddings is None:
        return 0

    existing = set(col.get()["ids"]) if col.count() > 0 else set()
    new_ids = []
    new_embeds = []
    new_texts = []
    new_metas = []
    for i, cid in enumerate(ids):
        if cid not in existing:
            new_ids.append(cid)
            new_embeds.append(embeddings[i])
            new_texts.append(texts[i])
            new_metas.append(metadatas[i])

    if new_ids:
        col.add(
            embeddings=new_embeds,
            documents=new_texts,
            metadatas=new_metas,
            ids=new_ids,
        )
    return len(new_ids)


def search_papers(query: str, top_k: int = 5, collection_name: str = "papers") -> list[dict]:
    col = get_collection(collection_name)
    if col is None or col.count() == 0:
        return []

    query_embedding = embed_texts([query])
    if query_embedding is None:
        return []

    try:
        results = col.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, col.count()),
        )
        papers = []
        for i in range(len(results["ids"][0])):
            papers.append({
                "title": results["metadatas"][0][i]["title"],
                "summary": results["documents"][0][i][:500],
                "source": results["metadatas"][0][i].get("source", "arxiv"),
                "score": round(results["distances"][0][i], 4) if results.get("distances") else 0.0,
            })
        return papers
    except Exception:
        return []
