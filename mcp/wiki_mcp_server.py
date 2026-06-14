import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI_DIR = ROOT / "wiki" / "ml"
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "about",
    "for",
    "how",
    "is",
    "of",
    "the",
    "to",
    "what",
    "why",
    "with",
    "가",
    "은",
    "는",
    "이",
    "란",
    "를",
    "을",
    "무엇",
    "뭐",
    "설명",
}


def parse_page(path):
    text = path.read_text(encoding="utf-8")
    meta = {"slug": path.stem, "title": path.stem, "tags": [], "updated": ""}
    body = text
    if text.startswith("---"):
        _, front, body = text.split("---", 2)
        for line in front.strip().splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "tags":
                meta[key] = [tag.strip(" []") for tag in value.strip("[]").split(",") if tag.strip()]
            else:
                meta[key] = value
    meta["path"] = str(path.relative_to(ROOT)).replace("\\", "/")
    meta["body"] = body.strip()
    return meta


def pages():
    return [parse_page(path) for path in sorted(WIKI_DIR.glob("*.md"))]


def score_page(page, query):
    q = query.lower().strip()
    if not q:
        return 1
    haystack = " ".join([page["title"], page["slug"], " ".join(page["tags"]), page["body"]]).lower()
    score = 0
    tokens = [
        token
        for token in re.findall(r"[a-zA-Z0-9가-힣-]+", q)
        if token not in STOPWORDS and (len(token) >= 3 or re.search(r"[A-Z]", token))
    ]
    title_slug_tags = " ".join([page["title"], page["slug"], " ".join(page["tags"])]).lower()
    for token in tokens:
        token = token.lower()
        score += haystack.count(token)
        if token in title_slug_tags:
            score += 25
        if token == page["slug"].lower():
            score += 50
    return score


def list_pages(args):
    return [
        {k: page[k] for k in ["title", "slug", "tags", "updated", "path"]}
        for page in pages()
    ]


def search_pages(args):
    query = args.get("query", "")
    ranked = sorted(
        ((score_page(page, query), page) for page in pages()),
        key=lambda item: item[0],
        reverse=True,
    )
    return [
        {
            "title": page["title"],
            "slug": page["slug"],
            "tags": page["tags"],
            "updated": page["updated"],
            "snippet": page["body"][:280].replace("\n", " "),
            "score": score,
        }
        for score, page in ranked
        if score > 0
    ]


def get_page(args):
    slug = args.get("slug", "")
    for page in pages():
        if page["slug"] == slug:
            return page
    raise ValueError(f"Page not found: {slug}")


def ask_wiki(args):
    question = args.get("question", "")
    normalized = question.lower().strip()

    identity_terms = ["이름", "누구", "정체", "who are you", "your name", "name"]
    likely_identity = "?" not in normalized and len(normalized) <= 20 and any(term in normalized for term in ["너", "agent", "에이전트"])
    if any(term in normalized for term in identity_terms) or likely_identity:
        return {
            "answer": (
                "저는 ML Wiki Agent입니다. 이 화면의 머신러닝 Wiki page를 MCP Tool로 검색하고, "
                "관련 page 근거를 바탕으로 질문에 답하거나 Wiki 유지보수 제안을 만드는 역할을 합니다."
            ),
            "sources": [
                {
                    "slug": "ml-index",
                    "title": "Machine Learning Wiki Index",
                    "snippet": "머신러닝 지식을 page 단위로 관리하고 변경을 추적하는 Wiki입니다.",
                }
            ],
        }

    matches = search_pages({"query": question})[:3]
    if not matches:
        return {
            "answer": (
                "Wiki에서 직접 연결되는 page를 찾지 못했습니다. "
                "Transformer, RAG, evaluation drift처럼 Wiki에 있는 개념으로 질문해 주세요."
            ),
            "sources": [],
        }

    primary = get_page({"slug": matches[0]["slug"]})
    first_para = next((p for p in primary["body"].split("\n\n") if p.strip() and not p.startswith("#")), "")
    answer = (
        f"'{primary['title']}' page 기준으로 보면, {first_para.strip()} "
        "관련 page를 함께 확인하면 개념 변화와 연결 관계를 더 잘 볼 수 있습니다."
    )
    return {
        "answer": answer,
        "sources": [{"slug": item["slug"], "title": item["title"], "snippet": item["snippet"]} for item in matches],
    }


TOOLS = {
    "list_pages": list_pages,
    "search_pages": search_pages,
    "get_page": get_page,
    "ask_wiki": ask_wiki,
}


def handle(request):
    method = request.get("method")
    if method == "tools/list":
        return {"tools": [{"name": name} for name in TOOLS]}
    if method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        if name not in TOOLS:
            raise ValueError(f"Unknown tool: {name}")
        return TOOLS[name](args)
    raise ValueError(f"Unknown method: {method}")


def main():
    raw = input()
    request = json.loads(raw)
    try:
        result = handle(request)
        print(json.dumps({"jsonrpc": "2.0", "id": request.get("id"), "result": result}, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"jsonrpc": "2.0", "id": request.get("id"), "error": {"message": str(exc)}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
