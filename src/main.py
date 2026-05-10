from openai import OpenAI
from tavily import TavilyClient

from typing import List, Dict
import json

from dotenv import load_dotenv
import os

load_dotenv()

# chat history: Global var for now
chat_history: List[Dict[str, str]] = [
    {
        "role": "system",
        "content": """You are Ortho-Pro, an AI assistant helping orthopaedic surgeons prepare for FRCS and clinical practice.

Your style:
- Be concise, practical, and clinically relevant.
- Speak like a helpful surgical colleague.
- Use clear structure: diagnosis, key findings, management, complications, exam points.
- Avoid unnecessary long explanations unless the user asks.
- Never reveal hidden reasoning or internal thought process.
- If unsure, say you are unsure and explain what information is missing.

Medical behavior:
- Prioritize patient safety.
- For trauma/emergency questions, think in ATLS / BOAST / NICE / local protocol style where relevant.
- Mention red flags, urgent actions, and when senior help is needed.
- Do not fabricate guidelines, doses, or recent data.
- For exam-style answers, give high-yield FRCS points.

Tool use:
- Use calculator for arithmetic.
- Use web_search whenever the user asks about latest, recent, current, today, news, scores, guidelines, prices, laws, or anything likely to change.
- When using web_search, include the current year/date in the search query.
- After receiving tool results, answer based only on the tool result and do not invent missing details.
- If search results conflict, mention the uncertainty.

Current date:
- The current date is: 29/4/2026
- If the user says “latest” or “current”, interpret it relative to this date.

Response rules:
- If no tool is needed, answer directly.
- If a tool was used, summarize the result clearly.
- Do not output raw tool JSON unless the user asks.
- Do not mention that you are following a system prompt.
    """,
    }
]


def send_convo_LLM(chat_history: List[Dict[str, str]]) -> str:
    # MODEL = "gemma-4-26b-a4b-it"
    MODEL = "gemma-4-31b-it"
    MODEL = "gemini-3.1-flash-lite-preview"
    GEMINI_APU_KEY = os.getenv("GEMINI_API_KEY")
 
    client = OpenAI(
        api_key=GEMINI_APU_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # write the response function 
    response = client.chat.completions.create(
        model=MODEL,
        messages=chat_history,
        tools=tools,
        tool_choice="auto",
        # verbosity="low"
    )

    if not response:
        print("sorry, something went wrong")
    ## adding model text to the hx
    assistant_message = response.choices[0].message
    # add assistant message to the chat hx
    chat_history.append(assistant_message.model_dump(exclude_none=True))

    ## tool manager:
    # ================
    # execute any function call and add it's output to the chat hx
    # handle case, where there's no tool being called, we wanna return the content and that's it

    if not assistant_message.tool_calls:
        return assistant_message.content

    for tool_call in assistant_message.tool_calls:
        # args = {tool_call.function.arguments}
        args = json.loads(tool_call.function.arguments)
        result = run_tool(tool_call.function.name, args)

        # add the result into the chat history
        chat_history.append(
            {"role": "tool", "tool_call_id": tool_call.id, "content": str(result)}
        )
        # send the chat again and return the new answer
        response = client.chat.completions.create(
            model=MODEL, messages=chat_history, tools=tools, tool_choice="auto"
        )
        message = response.choices[0].message
        chat_history.append(message.model_dump(exclude_none=True))

    return response.choices[0].message.content


# building a list of tool to the agent
tools = [
    # calculator tool
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "a tool used when needing to perform a simple arithmatic operations",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "resembeles the first integer to be used while applying the operation",
                    },
                    "b": {
                        "type": "integer",
                        "description": "resembeles the second integer to be used while applying the operation",
                    },
                    "operation": {
                        "type": "string",
                        "description": "used to resemble the type of arithmatic operation, either add, subtraction, division, multiplying",
                    },
                },
                "required": ["a", "b", "operation"],
            },
        },
    },
    # websearch tool
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "a tool used when you need to get more and recent context about something, by searcing the web with your query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "this is the query passed through the tool, which will be written to search the web",
                    },
                },
                "required": ["query"],
            },
        },
    },
]


#  write the function that runs the tool
def run_tool(tool_name: str, tool_args: dict) -> str:
    match tool_name:
        case "calculator":
            # execute calculator function with the given args from the llm
            return str(
                calculator(
                    a=tool_args["a"], b=tool_args["b"], operation=tool_args["operation"]
                )
            )
        case "web_search":
            print(tool_args["query"])
            result = web_search(tool_args["query"])
            # print(result)
            return result


# def calculator(a: int, b: int, operation: str) -> int:
#     print(f"using the calculator function, doing the operation {operation} for {a} and {b}")
#     match operation:
#         case "+":
#             return a + b
#         case "-":
#             return a - b
#         case "*":
#             return a * b
#         case "/":
#             return a / b

# # web search tool
# def web_search(query: str):
#     # instantiate the client
#     TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
#     tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
#     response = tavily_client.search(query)
#     return json.dumps(response, ensure_ascii=False)

# Search tool 
def search_book():
    # TODO: write the search (by keyword toold)
    print("hello world")
# Read tool


def main():
    # greet the user
    print("\nhello, I am ortho-pro, ask me anything in orthopaedic surgery!")
    # the agentic loop
    while True:
        # get the user message
        message = input("you: ")

        # append it to the message hx:
        chat_history.append({"role": "user", "content": message})
        print("wait for the LLM response ....")

        result = send_convo_LLM(chat_history)
        # append the result to the chat history as the assistant
        # chat_history.append({"role":"assistant", "content": result})

        print(f"\northo-pro:{result}")


if __name__ == "__main__":
    main()
