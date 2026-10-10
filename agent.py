from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from tools import calculator

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform basic mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "Mathematical operation"
                    }
                },
                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    }
]


def run_agent(question):

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:

        messages.append(message)

        for tool_call in message.tool_calls:

            if tool_call.function.name == "calculator":

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = calculator(
                    arguments["a"],
                    arguments["b"],
                    arguments["operation"]
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    }
                )

        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )

        return final_response.choices[0].message.content

    else:

        return message.content
