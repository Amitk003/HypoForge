import requests
import xml.etree.ElementTree as ET
from typing import Optional

from src.rag_index import index_papers as rag_index_papers, search_papers as rag_search_papers


def build_search_queries(research_goal: str) -> list[str]:
    """Cleans and extracts core search phrases from research goals."""
    stopwords = {"how", "does", "the", "what", "is", "an", "and", "or", "to", "in", "on", "of", "for", "with", "a"}  # noqa: E501
    words = [w.strip("?,.:;!") for w in research_goal.split()]
    filtered = [w for w in words if w.lower() not in stopwords and len(w) > 2]
    
    queries = []
    if filtered:
        queries.append(" ".join(filtered[:4]))
        if len(filtered) > 4:
            queries.append(" ".join(filtered[4:8]))
    
    clean_goal = " ".join(filtered[:6])
    if clean_goal and clean_goal not in queries:
        queries.append(clean_goal)
        
    return queries if queries else [research_goal]


def fetch_arxiv_papers(query: str, max_results: int = 5) -> list[dict]:
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }
    headers = {"User-Agent": "HypoForge/1.0"}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        if resp.status_code != 200:
            return []
            
        root = ET.fromstring(resp.content)
        # Atom feed namespace
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        
        for entry in root.findall("atom:entry", ns):
            title_elem = entry.find("atom:title", ns)
            summary_elem = entry.find("atom:summary", ns)
            
            title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else ""
            summary = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""
            
            if title:
                papers.append({
                    "title": title,
                    "summary": summary[:500],
                    "source": "arxiv"
                })
        return papers
    except Exception as e:
        return [{"title": f"Notice: Search query fallback ({e})", "summary": "", "source": "error"}]


def search_papers(research_goal: str, max_papers: int = 10) -> list[dict]:
    queries = build_search_queries(research_goal)
    all_papers = []
    per_query = max(max_papers // max(len(queries), 1), 3)
    
    for q in queries[:3]:
        papers = fetch_arxiv_papers(q, max_results=per_query)
        all_papers.extend([p for p in papers if p.get("source") != "error"])
        
    seen = set()
    unique = []
    for p in all_papers:
        if p["title"].lower() not in seen:
            seen.add(p["title"].lower())
            unique.append(p)
            
    return unique[:max_papers]


def format_papers_for_context(papers: list[dict]) -> str:
    if not papers:
        return "No literature found."
    lines = ["Relevant papers found:"]
    for i, p in enumerate(papers, 1):
        lines.append(f"\n{i}. {p['title']}")
        if p.get("summary"):
            lines.append(f"   {p['summary'][:300]}...")
        if p.get("score") is not None:
            lines.append(f"   (semantic relevance: {p['score']})")
    return "\n".join(lines)


def search_with_rag(research_goal: str, max_papers: int = 10) -> list[dict]:
    raw_papers = search_papers(research_goal, max_papers=max_papers)
    if raw_papers:
        rag_index_papers(raw_papers)
    ranked = rag_search_papers(research_goal, top_k=max_papers)
    if ranked:
        return ranked
    return raw_papers

