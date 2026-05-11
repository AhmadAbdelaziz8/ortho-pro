from pathlib import Path
import json
import time


def search(keywords: list[str], limit: int = 5) -> list[dict]:
    start_time = time.perf_counter()

    pages_dir = Path("data/pages_data")
    keywords_normalised = [keyword.lower() for keyword in keywords]

    final_result = []

    for page_dir in pages_dir.glob("*.json"):
        score = 0
        snippet = []

        with open(page_dir, "r", encoding="utf-8") as f:
            page_data = json.load(f)

        chunks = page_data["chunks"]

        for chunk_dict in chunks:
            chunk_content = chunk_dict["content"]
            chunk_id = chunk_dict["id"]

            chunk_content_lower = chunk_content.lower()

            matched_keywords = [
                keyword
                for keyword in keywords_normalised
                if keyword in chunk_content_lower
            ]

            if matched_keywords:
                score += len(matched_keywords)

                snippet.append(
                    {
                        "chunk_id": chunk_id,
                        "matched_keywords": matched_keywords,
                        "content": chunk_content,
                    }
                )

        if score > 0:
            final_result.append(
                {
                    "page_number": page_data["page_number"],
                    "score": score,
                    "snippet": snippet,
                }
            )

    final_result.sort(
        key=lambda result: (result["score"], result["page_number"]), reverse=True
    )

    execution_time = time.perf_counter() - start_time
    print(f"execution time: {execution_time:.4f} seconds")

    return final_result[:limit]


if __name__ == "__main__":
    results = search(["colles", "management"])

    for result in results:
        print(f"\npage: {result['page_number']}, score: {result['score']}")

        for snippet in result["snippet"][:3]:
            print(f"chunk: {snippet['chunk_id']}")
            print(f"matched: {snippet['matched_keywords']}")
            print(snippet["content"])
            print("-" * 50)