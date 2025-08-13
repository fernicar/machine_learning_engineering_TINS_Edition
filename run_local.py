"""Run the Machine Learning Engineering Agent locally."""

import asyncio
import dotenv
import os
import sys
import textwrap

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from google.genai import types
from google.adk.runners import InMemoryRunner
from machine_learning_engineering.agent import root_agent

async def main():
    """Runs the agent locally in an interactive chat session."""
    dotenv.load_dotenv()
    app_name = "machine-learning-engineering"
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    print("Starting local chat session with the agent.")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        content = types.Content(parts=[types.Part(text=user_input)], role="user")
        response = ""
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts and event.content.parts[0].text:
                response_part = event.content.parts[0].text
                print(f"Agent: {response_part}")
                response += response_part

    print("Chat session ended.")

if __name__ == "__main__":
    asyncio.run(main())
