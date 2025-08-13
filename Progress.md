# Plan to Adapt the Project for Free Tier Usage

This document outlines the plan to adapt the project to run using only the free services provided by Google AI Studio, removing the dependencies on paid Google Cloud and VertexAI services.

## Phase 1: Remove Vertex AI Deployment

The project currently includes code for deploying the agent to Vertex AI, which is a paid service. This functionality needs to be removed.

-   [x] **Remove the `deployment` directory:** This directory contains scripts for deploying and testing the agent on Vertex AI. It should be removed entirely.
-   [x] **Update `pyproject.toml`:** Remove the `google-cloud-aiplatform` dependency from `pyproject.toml`, as it is related to Vertex AI.

## Phase 2: Adapt the Agent for Local Execution

The agent is built using the Google ADK. We need to ensure that it can be run locally without relying on Vertex AI for execution.

-   [x] **Verify local execution:** The `tests/test_agents.py` file uses `InMemoryRunner` to run the agent locally. We need to build on this and create a simple script to run the agent locally for development and testing. This script would replace the functionality of `deployment/test_deployment.py`.
-   [x] **Update documentation:** The `README.md` should be updated to explain how to run the agent locally, without mentioning Vertex AI deployment.

## Phase 3: Use Google AI Studio for the LLM

The project uses `google.genai` to interact with the language model. This can be configured to use the free tier of the Gemini API from Google AI Studio.

-   [x] **Confirm API key usage:** Ensure that the project can be configured with an API key from Google AI Studio. The use of `dotenv` and `os.environ.get("ROOT_AGENT_MODEL")` suggests that this is already possible.
-   [x] **Update documentation:** The `README.md` should be updated to explain how to get an API key from Google AI Studio and configure the project to use it.

By following this plan, the project will be adapted to run using only the free services from Google AI Studio, making it accessible for learning and experimentation without incurring any costs.
