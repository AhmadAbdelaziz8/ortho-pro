from pathlib import Path
import json


def read(page_number: int) -> dict:

    pages_dir = Path("data/pages_data")
    #
    with open(pages_dir / f"page_{page_number}.json", "r") as f:
        page_data = json.load(f)
        result = {
            "page_number": page_data["page_number"],
            # "paragraphs": page_data["paragraphs"],
            "content": page_data["chunks"]
        }
        print(result)
        return result 

if __name__ == "__main__":
    read(80)