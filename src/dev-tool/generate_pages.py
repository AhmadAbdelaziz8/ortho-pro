import pymupdf as pm
import json
from pathlib import Path


# load mcrea
def load_mcrea():
    # step 1:
    MCREA_PATH = "books/McRae's Orthopaedic Trauma andEmergency Fracture_Management.pdf"
    try:
        mcrea_doc = pm.open(filename=MCREA_PATH, filetype="pdf")
        total_pages = mcrea_doc.page_count
        print(f"total page count is : {total_pages}")
        print(type(mcrea_doc))

        return mcrea_doc

    except Exception as e:
        print(e)
    # loop over the pages,


# generate pages
def generate_pages(mcrea_doc):
    # loop over pages, and for each page, create a json file, that contains it's the page number and the
    # paragraphs, each paragraph is separated by /n/n
    DOC_PATH = Path("/Users/ahmad-ali/repos/ortho-pro/data/pages_data")
    # create a folder for that path if doesn't exist
    DOC_PATH.mkdir(parents=True, exist_ok= True)
    CHUNK_SIZE = 120

    page_count = mcrea_doc.page_count
    for page_index in range(page_count):
        page_chunks = []
        page = mcrea_doc[page_index]
        page_text = page.get_text("text")

        # clean text 
        page_text = page_text.replace("\n", " ")
        page_text = page_text.replace("\t", " ")
        page_text = page_text.replace("\u00ad", " ")
        words = page_text.split()
        # chunks variables
        chunk_no = 1
        chunk_content = " "
        chunk_words_count = 0
        #generate chunkgs foreach 20 words
        for word_index, word in enumerate(words): 
            # start_index = word_index
            # end_index = words.length 

            if chunk_words_count < CHUNK_SIZE: 
                chunk_content += word + " "
                chunk_words_count += 1    
            else: 
                chunk = {
                    "id": chunk_no,
                    "content": chunk_content,
                }
                page_chunks.append(chunk)
                chunk_no += 1
                chunk_content = word + " "
                chunk_words_count = 0

        # create the page object
        page_content = {"page_number": page_index + 1, "chunks":page_chunks }
        file_path = DOC_PATH / f"page_{page_index + 1}.json"
        
        # open the doc and save the dict there,
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(page_content, file, ensure_ascii=False, indent=2)
            # print(f"page {page_index + 1} has been saved successfully")


if __name__ == "__main__":
    doc = load_mcrea()
    generate_pages(doc)
