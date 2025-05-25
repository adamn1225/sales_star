import os
from dataclasses import dataclass
from typing import Literal, Optional
import openai
import dotenv

getenv = dotenv.load_dotenv("OPENAI_API_KEY")

def web_search(query, user_location=None, search_context_size="medium"):
    # Simulate a web search result for demonstration
    return (
        f"Simulated web search results for '{query}'"
        f"{' in ' + user_location if user_location else ''} "
        f"(context: {search_context_size})"
    )
def email_finder(name, company_domain):
    # Simulate an email pattern
    first, last = name.lower().split()
    email = f"{first}.{last}@{company_domain}".replace(" ", "")
    return f"Likely email for {name} at {company_domain}: {email}"

@dataclass
class WebSearchTool:
    user_location: Optional[str] = None
    search_context_size: Literal["low", "medium", "high"] = "medium"

    def search(self, query: str) -> str:
        # In a real implementation, this would call a web search API.
        # Here, we'll simulate a result.
        return f"Simulated web search results for '{query}' (location: {self.user_location}, context: {self.search_context_size})"

class Agent:
    def __init__(self, name, instructions, handoff_description=None):
        self.name = name
        self.instructions = instructions
        self.handoff_description = handoff_description

class Runner:
    @staticmethod
    def run_sync(agent, prompt):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": (
                        "Search the web for up-to-date information about companies, people, or topics. "
                        "Use this to find recent news, company background, decision makers, or prospecting insights."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "The search query"},
                            "user_location": {"type": "string", "description": "Location for search relevance", "default": None},
                            "search_context_size": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Amount of context to use for the search",
                                "default": "medium",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
            "type": "function",
            "function": {
                "name": "email_finder",
                "description": "Find a likely email address for a person at a company.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Full name of the person"},
                    "company_domain": {"type": "string", "description": "Company's domain, e.g., example.com"},
            },
            "required": ["name", "company_domain"],
        },
    },
}
        ]

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": agent.instructions},
                {"role": "user", "content": prompt}
            ],
            tools=tools,
            tool_choice="auto",
            max_tokens=200,
            temperature=0.6,
        )

        message = response.choices[0].message
        if hasattr(message, "tool_calls") and message.tool_calls:
            import json
            tool_messages = []
            for tool_call in message.tool_calls:
                parsed_args = json.loads(tool_call.function.arguments)
                if tool_call.function.name == "web_search":
                    tool_result = web_search(
                        parsed_args["query"],
                        parsed_args.get("user_location"),
                        parsed_args.get("search_context_size", "medium")
                    )
                elif tool_call.function.name == "email_finder":
                    tool_result = email_finder(
                        parsed_args["name"],
                        parsed_args["company_domain"]
                    )
                else:
                    tool_result = "Tool not implemented."
                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": tool_result,
                })
            # Now send all tool messages in the follow-up
            followup = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": agent.instructions},
                    {"role": "user", "content": prompt},
                    {
                        "role": "assistant",
                        "content": message.content or "",
                        "tool_calls": [tc.to_dict() for tc in (message.tool_calls or [])],
                    },
                    *tool_messages,
                ],
                max_tokens=500,
                temperature=0.7,
            )
            class Result:
                final_output = followup.choices[0].message.content.strip()
            return Result()
        class Result:
            final_output = message.content.strip()
        return Result()