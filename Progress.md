# Plan to Remove Google Cloud and VertexAI Dependencies

This document outlines the plan to remove the dependencies on Google Cloud and VertexAI from this project. The goal is to make the project cloud-agnostic and capable of running with other large language models and deployment platforms.

## Phase 1: Replace the Agent Development Kit (ADK)

The project is heavily dependent on the Google Agent Development Kit (ADK). To remove this dependency, we need to replace it with a different agent framework or build a custom one.

-   [ ] **Research alternative agent frameworks:** Investigate open-source agent frameworks that provide similar functionality to the Google ADK. Examples include LangChain, LlamaIndex, and AutoGen.
-   [ ] **Select a new agent framework:** Choose a framework that best fits the needs of the project.
-   [ ] **Refactor the agent definitions:** Rewrite the agent definitions in `machine_learning_engineering/agent.py` and the sub-agents to use the new framework. This will involve changing the base classes for the agents (`Agent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`) and the way they are composed.
-   [ ] **Refactor the callback functions:** Rewrite the callback functions to be compatible with the new framework. This includes functions for state management, prompt generation, and processing the LLM's response.
-   [ ] **Refactor the tool usage:** Replace the usage of `google_search` with a similar tool from the new framework or a custom implementation.

## Phase 2: Replace the Generative AI Model

The project uses `google.genai` to interact with Google's generative AI models. This needs to be replaced with a more general solution that can work with different models.

-   [ ] **Abstract the model interface:** Create a common interface for interacting with large language models. This interface should define methods for generating text, and it should be possible to implement it for different models (e.g., OpenAI's GPT models, Anthropic's Claude models, or local models).
-   [ ] **Implement the model interface for different models:** Create implementations of the model interface for the desired models.
-   [ ] **Update the agent code to use the model interface:** Modify the agent code to use the new model interface instead of directly calling `google.genai`. This will make it easy to switch between different models.

## Phase 3: Replace the Deployment and Evaluation Logic

The `deployment` and `eval` directories contain code for deploying and evaluating the agent on Vertex AI. This needs to be replaced with a more general solution.

-   [ ] **Remove the `deployment` directory:** The `deployment` directory is specific to Vertex AI and can be removed. A new deployment solution will need to be created depending on the target platform.
-   [ ] **Refactor the evaluation logic:** The evaluation logic in the `eval` directory uses the `AgentEvaluator` from the Google ADK. This needs to be rewritten to use the new agent framework and evaluation methods. This might involve creating a custom evaluation script or using the evaluation tools provided by the new framework.

## Phase 4: Update the Dependencies

-   [ ] **Update `pyproject.toml`:** Remove the dependencies on `google-adk`, `google-genai`, and `google-cloud-aiplatform` from `pyproject.toml`.
-   [ ] **Add new dependencies:** Add the dependencies for the new agent framework and any other new libraries that are used.

This plan is a high-level overview of the steps required to remove the dependencies on Google Cloud and VertexAI. Each step will require significant effort and careful planning.
