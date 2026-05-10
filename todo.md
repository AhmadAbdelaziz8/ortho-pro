# TODO

## search tool [done] 
 - params: (query: list of strings)
 - output: dict, contains page_number, snippet, score 

## read tool 
 - params: page number: integer
 - output: dict {key: paragraph_no, value: string contains paragraph's text}


# DONE
## [x] turn the book into folder of json files
    - infinite loop
    - read the book 
    - save it into json file, each one is a page
    - foreach page, save it's contents as paragraphs

## [x] chatbot: 


    - exit with a way I want to use
    - openAI format 
    - using gemma

    =========
    steps: 
    - the user writes message, 
    - message is appended to the convsersation, then it's being sent to the llm, 
    - add the llm response to it and display it

