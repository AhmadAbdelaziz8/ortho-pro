from openai import OpenAI
from typing import List, Dict

from dotenv import load_dotenv
import os
load_dotenv()

# chat history: Global var for now 
chat_history: List[Dict[str,str]] = [
    {"""role": "system", "content": "you are helping orthopaedic surgeons to learn for FRCS, 
        make your response as concise as possible
    """}
]

def send_convo_LLM(chat_history:List[Dict[str, str]]) -> str:
    # MODEL = "gemma-4-26b-a4b-it"
    MODEL = "gemma-4-31b-it"
    GEMINI_APU_KEY = os.getenv("GEMINI_API_KEY")

    client = OpenAI(
        api_key=GEMINI_APU_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # write the response function 
    response = client.chat.completions.create(
        model = MODEL,
        messages= chat_history,
    )

    return response.choices[0].message.content

    
def main():
    # greet the user 
    print("\nhello, I am ortho-pro, ask me anything in orthopaedic surgery!")
    # the agentic loop
    while True: 
        # get the user message 
        message = input("you: ") 
        
        # append it to the message hx: 
        chat_history.append({"role":"user", "content": message})
        print("wait for the LLM response ....")

        result = send_convo_LLM(chat_history)
        print(f"\northo-pro:{result}")


if __name__ == "__main__":
    main()
