from typing import Optional
import requests
import json


def build_search_queries(research_goal: str) -> list[str]:
    keywords = research_goal.lower().replace("?", "").replace(",", "").split()
    keywords = [k for k in keywords if len(k) > 3]
    mid = len(keywords) // 2
    queries = []
    if len(keywords) >= 4:
        queries.append(" ".join(keywords[:mid]))
        queries.append(" ".join(keywords[mid:]))
    queries.append(" ".join(keywords[:5]))
    queries = [q for q in queries if q.strip()]
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
        papers = []
        entries = resp.text.split("<entry>")
        for entry in entries[1:]:
            title = ""
            summary = ""
            if "<title>" in entry:
                title = entry.split("<title>")[1].split("</title>")[0].strip()
            if "<summary>" in entry:
                summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
            if title:
                papers.append({"title": title, "summary": summary[:500], "source": "arxiv"})
        return papers
    except Exception as e:
        return [{"title": f"Error fetching papers: {e}", "summary": "", "source": "error"}]


def search_papers(research_goal: str, max_papers: int = 10) -> list[dict]:
    queries = build_search_queries(research_goal)
    all_papers = []
    for q in queries[:3]:
        papers = fetch_arxiv_papers(q, max_results=max(max_papers // len(queries), 2))
        all_papers.extend(papers)
    seen = set()
    unique = []
    for p in all_papers:
        if p["title"] not in seen:
            seen.add(p["title"])
            unique.append(p)
    return unique[:max_papers]


def format_papers_for_context(papers: list[dict]) -> str:
    if not papers:
        return "No literature found."
    lines = ["Relevant papers found:"]
    for i, p in enumerate(papers, 1):
        lines.append(f"\n{i}. {p['title']}")
        if p.get("summary"):
            lines.append(f"   {p['summary'][:300]}")
    return "\n".join(lines)
