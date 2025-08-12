# TINS for this Python Project

## Description

[General description of the software]

## Functionality

[Detailed functionality sections]

## Technical Implementation

[Technical details sections]

## File Structure

```
.:
LICENSE
README.md
deployment
eval
machine-learning-engineering-architecture.svg
machine_learning_engineering
pyproject.toml
tests

./deployment:
__init__.py
deploy.py
test_deployment.py

./eval:
__init__.py
full_eval
simple_eval

./eval/full_eval:
__init__.py
full.test.json
test_config.json
test_eval.py

./eval/simple_eval:
__init__.py
simple.test.json
test_config.json
test_eval.py

./machine_learning_engineering:
__init__.py
agent.py
prompt.py
shared_libraries
sub_agents
tasks

./machine_learning_engineering/shared_libraries:
__init__.py
check_leakage_util.py
code_util.py
common_util.py
config.py
data_leakage_prompt.py
debug_prompt.py
debug_util.py

./machine_learning_engineering/sub_agents:
ensemble
initialization
refinement
submission

./machine_learning_engineering/sub_agents/ensemble:
__init__.py
agent.py
prompt.py

./machine_learning_engineering/sub_agents/initialization:
__init__.py
agent.py
prompt.py

./machine_learning_engineering/sub_agents/refinement:
__init__.py
agent.py
prompt.py

./machine_learning_engineering/sub_agents/submission:
__init__.py
agent.py
prompt.py

./machine_learning_engineering/tasks:
california-housing-prices

./machine_learning_engineering/tasks/california-housing-prices:
task_description.txt
test.csv
train.csv

./tests:
test_agents.py
```

## Python Files Description

### `deployment/deploy.py`

This script handles the deployment of the Machine Learning Engineering Agent to Google Cloud Vertex AI.

**Functionality:**

- **Creates a new agent engine:** It defines the agent's dependencies and creates a new agent engine on Vertex AI.
- **Deletes an existing agent engine:** It can delete an agent engine given its resource ID.
- **Lists all agent engines:** It can list all the agent engines in the specified GCP project and location.

**Usage:**

The script is run from the command line and accepts the following flags:

- `--project_id`: The GCP project ID.
- `--location`: The GCP location.
- `--bucket`: The GCP bucket for staging.
- `--resource_id`: The resource ID of the agent to be deleted.
- `--create`: A boolean flag to create a new agent.
- `--delete`: A boolean flag to delete an existing agent.
- `--list`: A boolean flag to list all agents.

The script initializes the Vertex AI client with the provided credentials and then performs the requested action. It also loads environment variables from a `.env` file.

### `deployment/test_deployment.py`

This script is used to test a deployed Machine Learning Engineering Agent on Google Cloud Vertex AI.

**Functionality:**

- **Connects to a deployed agent:** It takes a resource ID of a deployed agent and connects to it.
- **Creates a user session:** It creates a new session for a given user ID.
- **Interactive chat:** It provides an interactive command-line interface to chat with the agent. You can type messages, and the agent's responses will be printed to the console.
- **Deletes the user session:** When the user types "quit", the script deletes the session.

**Usage:**

The script is run from the command line and accepts the following flags:

- `--project_id`: The GCP project ID.
- `--location`: The GCP location.
- `--bucket`: The GCP bucket for staging.
- `--resource_id`: The resource ID of the deployed agent.
- `--user_id`: A unique identifier for the user.

The script initializes the Vertex AI client, gets the remote agent, creates a session, and then enters a loop to stream queries to the agent and print the responses.

### `eval/full_eval/test_eval.py`

This is a pytest script for running a "full" evaluation of the Machine Learning Engineering Agent.

**Functionality:**

- **Loads environment variables:** It uses `dotenv` to load environment variables.
- **Runs an agent evaluation:** It uses the `AgentEvaluator` from the Google ADK to evaluate the agent based on a test case defined in `full.test.json`.
- **Asynchronous test:** The test is an `async` function and uses `pytest-asyncio`.
- **Sets a timeout:** It sets the execution timeout for the agent to 30 seconds.

**Usage:**

This script is meant to be run with `pytest`. It will automatically discover and run the `test_full_interaction` test.

### `eval/simple_eval/test_eval.py`

This is a pytest script for running a "simple" evaluation of the Machine Learning Engineering Agent.

**Functionality:**

- **Loads environment variables:** It uses `dotenv` to load environment variables.
- **Runs an agent evaluation:** It uses the `AgentEvaluator` from the Google ADK to evaluate the agent based on a test case defined in `simple.test.json`.
- **Asynchronous test:** The test is an `async` function and uses `pytest-asyncio`.

**Usage:**

This script is meant to be run with `pytest`. It will automatically discover and run the `test_basic_interaction` test. It is similar to the `full_eval` script, but uses a different test set.

### `machine_learning_engineering/agent.py`

This file defines the main agent for the Machine Learning Engineering (MLE) task. It orchestrates a sequence of sub-agents to solve the task.

**Functionality:**

- **Defines a sequential agent:** It creates a `SequentialAgent` named `mle_pipeline_agent` that runs a series of sub-agents in a specific order.
- **Composes sub-agents:** The pipeline consists of four sub-agents:
    1.  `initialization_agent`: To set up the task.
    2.  `refinement_agent`: To refine the solution.
    3.  `ensemble_agent`: To combine different models.
    4.  `submission_agent`: To generate the final submission.
- **Saves agent state:** After each sub-agent in the pipeline completes, a callback function `save_state` is triggered to save the current state of the agent to a `final_state.json` file.
- **Defines a root agent:** It defines a `root_agent` which is the main entry point for the ADK. This agent has a system instruction and a front-door instruction to route the user's request to the `mle_pipeline_agent`.

**Architecture:**

The overall architecture is a pipeline of specialized agents, with a front-door agent to manage the interaction. This modular design allows for a clear separation of concerns, with each sub-agent responsible for a specific part of the MLE task.

### `machine_learning_engineering/prompt.py`

This file contains all the prompts used by the Machine Learning Engineering Agent and its sub-agents.

**Prompts:**

- **`SYSTEM_INSTRUCTION`**: This is a high-level instruction for the entire multi-agent system, defining its identity as a "Machine Learning Engineering Multi Agent System".
- **`FRONTDOOR_INSTRUCTION`**: This prompt guides the `root_agent`. It instructs the agent on how to interact with the user, how to handle direct questions, and when to delegate the task to the `mle_pipeline_agent`. It also defines the workflow for the agent.
- **`TASK_AGENT_INSTR`**: This prompt provides instructions for the agents that are responsible for the actual machine learning task. It sets the persona of a "Kaggle grandmaster" and outlines the goal of the competition.

These prompts are crucial for guiding the behavior of the large language models that power the agents.

### `machine_learning_engineering/shared_libraries/check_leakage_util.py`

This file contains utility functions for creating an agent that checks for and corrects data leakage in Python code.

**Functionality:**

- **Creates a data leakage checker agent:** The main function `get_data_leakage_checker_agent` constructs a `SequentialAgent` that is responsible for identifying and fixing data leakage.
- **Agent Composition:** The data leakage agent is composed of two sub-agents:
    1.  `check_leakage_loop_agent`: This agent repeatedly checks the code for data leakage until it can successfully parse the leakage status from the model's response.
    2.  `refine_leakage_agent`: If data leakage is detected, this agent is invoked to refine the code and fix the issue.
- **Dynamic prompt generation:** Functions like `get_check_leakage_agent_instruction` and `get_refine_leakage_agent_instruction` dynamically generate prompts for the agents based on the current code.
- **Callback-driven logic:** The utility uses a series of callback functions to manage the flow of the data leakage check and correction process. These callbacks handle tasks like parsing the model's response, updating the agent's state, and replacing the problematic code.
- **Self-correction loop:** This utility implements a self-correction mechanism where the agent can identify a problem (data leakage), and then attempt to fix it automatically.

**Architecture:**

The utility is designed to be a self-contained module that can be easily integrated into a larger agentic system. It uses the Google ADK's `Agent`, `SequentialAgent`, and `LoopAgent` classes to create a robust and reliable data leakage detection and correction system.

### `machine_learning_engineering/shared_libraries/code_util.py`

This file provides a collection of utility functions for executing Python code, managing agent state, and evaluating the performance of the generated code.

**Functionality:**

- **Code Execution:**
    - `run_python_code`: This function takes a string of Python code, saves it to a file, and executes it in a sandboxed environment using `subprocess.run`. It captures the standard output, standard error, and execution time.
- **Performance Extraction:**
    - `extract_performance_from_text`: This function parses the output of the executed code to extract the "Final Validation Performance" score.
- **State Management:**
    - `get_name_with_prefix_and_suffix`: A helper function to create unique names for state variables.
    - `get_updated_suffix`: Generates a suffix for state keys based on the current agent and its state, allowing for fine-grained state management in a multi-agent system.
    - `get_code_state_key` and `get_code_execution_result_state_key`: These functions determine the appropriate keys for storing the code and its execution results in the agent's state.
- **Conditional Execution:**
    - `get_run_code_condition`: This function defines the conditions under which the generated code should be executed. This is used to prevent unnecessary code execution.
- **Code Evaluation:**
    - `evaluate_code`: This is the main function that orchestrates the code evaluation process. It retrieves the code from the state, decides whether to run it, executes it, extracts the performance, and stores the results back in the state.

**Architecture:**

This file is a crucial part of the agent's ability to write and test its own code. It provides the low-level functionality needed to execute code and the high-level logic to manage the evaluation process. The use of state management functions allows the agent to keep track of its progress and the performance of different versions of the code.

### `machine_learning_engineering/shared_libraries/common_util.py`

This file contains a set of common utility functions that are used throughout the project.

**Functionality:**

- **`get_text_from_response`**: Extracts the text content from a `LlmResponse` object. This is a helper function to simplify the process of working with the output of the language model.
- **`set_random_seed`**: Sets the random seed for various libraries (`random`, `numpy`, `torch`) to ensure that experiments are reproducible.
- **`copy_file`**: A simple utility function to copy a file from a source path to a destination directory.

These are general-purpose functions that provide common functionality needed by different parts of the agent system.

### `machine_learning_engineering/shared_libraries/config.py`

This file defines the configuration for the Machine Learning Engineering Agent.

**Functionality:**

- **Defines a configuration class:** It uses a `dataclass` called `DefaultConfig` to define all the configuration parameters for the agent.
- **Provides default values:** Each parameter in the `DefaultConfig` class has a default value.
- **Centralized configuration:** This file provides a single, centralized location for all the configuration parameters, making it easy to manage and modify the agent's behavior.
- **Environment variable support:** The `agent_model` is configured using an environment variable `ROOT_AGENT_MODEL`, with a fallback to a default value.

**Configuration Parameters:**

The configuration includes parameters for:

- **Task specification:** `data_dir`, `task_name`, `task_type`, `task_description`, `task_summary`.
- **Workspace and models:** `workspace_dir`, `agent_model`.
- **Execution control:** `exec_timeout`, `seed`, `max_retry`, `max_debug_round`, `max_rollback_round`.
- **Agent behavior:** `num_solutions`, `num_model_candidates`, `inner_loop_round`, `outer_loop_round`, `ensemble_loop_round`, `num_top_plans`.
- **Feature flags:** `use_data_leakage_checker`, `use_data_usage_checker`.

An instance of the `DefaultConfig` class is created as `CONFIG`, which is then imported and used by other modules in the project.

### `machine_learning_engineering/shared_libraries/data_leakage_prompt.py`

This file defines the prompts used by the data leakage checker agent.

**Prompts:**

- **`CHECK_LEAKAGE_INSTR`**: This prompt is used to instruct a large language model to analyze a given Python code block and identify potential data leakage. It specifically asks the model to check for common data leakage scenarios, such as using validation or test data to influence the training process. The expected output is a JSON object with the leakage status and the problematic code block.
- **`LEAKAGE_REFINE_INSTR`**: This prompt is used when data leakage has been detected. It instructs the language model to refine the code to fix the data leakage issue. The expected output is a markdown code block containing the corrected code.

These prompts are essential for the self-correction mechanism of the data leakage checker. They provide the language model with clear instructions on how to identify and fix data leakage problems in the generated code.

### `machine_learning_engineering/shared_libraries/debug_prompt.py`

This file defines the prompts used by the debugging agent.

**Prompts:**

- **`BUG_SUMMARY_INSTR`**: This prompt is used to instruct a large language model to summarize an error report. The goal is to extract the most relevant information from the error message, making it easier for the agent to understand the problem.
- **`BUG_REFINE_INSTR`**: This prompt is used to instruct the language model to fix a bug in a given Python script. It provides the model with the task description, the buggy code, and the error message. The prompt also includes specific instructions on how to format the output, how to handle `ModuleNotFoundError`, and to ensure that the corrected code is self-contained and includes a line to print the final validation performance.

These prompts are the core of the agent's self-debugging capabilities. They enable the agent to understand and fix errors in the code it generates, which is a crucial part of the autonomous machine learning engineering process.

### `machine_learning_engineering/shared_libraries/debug_util.py`

This file provides utility functions for creating and managing debugging agents. It is the core of the self-healing capabilities of the system.

**Functionality:**

- **Creates a run-and-debug agent:** The main function `get_run_and_debug_agent` constructs a complex `LoopAgent` that can run a given task, and if it fails, it will automatically try to debug it.
- **Agent Composition:** The run-and-debug agent is composed of several sub-agents:
    - A `run_loop_agent` that repeatedly tries to execute the main task.
    - A `debug_inner_loop_agent` that is invoked if the `run_loop_agent` fails. This agent first summarizes the bug and then enters a loop to try and fix it.
- **Optional Data Leakage Checking:** The `run_and_debug_agent` can be configured to include a data leakage checker agent in its execution pipeline.
- **Callback-driven debugging:** The debugging process is managed by a series of callback functions that handle tasks like checking for rollbacks, summarizing bugs, and updating the code with the fixes provided by the language model.
- **Dynamic prompt generation:** The prompts for the debugging agents are generated dynamically based on the current context, including the code, the error message, and the task description.

**Architecture:**

This utility provides a powerful framework for building self-healing agents. By combining code execution, data leakage checking, and automated debugging, it creates a robust system that can autonomously generate and refine machine learning solutions. The use of nested `LoopAgent` and `SequentialAgent` allows for a flexible and powerful control flow.

### `machine_learning_engineering/sub_agents/ensemble/agent.py`

This file defines the ensembling agent, which is responsible for combining multiple machine learning solutions to create a more robust and accurate model.

**Functionality:**

- **Creates an ensembling plan:** The agent starts by generating an initial plan on how to ensemble the different solutions that have been generated by the previous agents.
- **Implements the ensembling plan:** It then implements this plan, generating a new Python script that combines the models.
- **Iteratively refines the plan:** The agent then enters a loop where it refines the ensembling plan based on the performance of the previous attempts, and then implements the refined plan.
- **Workspace management:** Before starting the ensembling process, it creates a dedicated workspace for the ensembling task, copying all the necessary data files.
- **Dynamic prompt generation:** The prompts for the ensembling agents are generated dynamically, providing the language model with the context of the existing solutions and the previous ensembling attempts.
- **Self-healing:** The implementation of the ensembling plans is done using a `run_and_debug_agent` from `debug_util.py`, which means that if the ensembling script has any bugs, the agent will automatically try to fix them.

**Architecture:**

The ensembling agent is a `SequentialAgent` that follows a structured process of planning, implementation, and refinement. It uses a `LoopAgent` to iteratively improve the ensembling strategy. This modular and iterative approach allows the agent to systematically explore different ensembling techniques and converge on a high-performing solution.

### `machine_learning_engineering/sub_agents/ensemble/prompt.py`

This file defines the prompts used by the ensembling agent.

**Prompts:**

- **`INIT_ENSEMBLE_PLAN_INSTR`**: This prompt is used to instruct a large language model to create an initial plan for ensembling a set of given Python solutions. The prompt sets the persona of a "Kaggle grandmaster" and asks for a plan that is novel, effective, and easy to implement.
- **`ENSEMBLE_PLAN_IMPLEMENT_INSTR`**: This prompt instructs the language model to implement a given ensembling plan. It provides the model with the Python solutions and the plan, and asks for a single, self-contained Python script that implements the ensembling strategy. The prompt also specifies the output format, including the requirement to print the final validation performance.
- **`ENSEMBLE_PLAN_REFINE_INSTR`**: This prompt is used to ask the language model to refine an existing ensembling plan. It provides the model with the previous plans and their scores, and asks for a new, improved plan that is likely to achieve a better score.

These prompts are the driving force behind the ensembling agent's ability to generate and iteratively improve its ensembling strategies. They provide the language model with the necessary context and instructions to perform the complex task of ensembling different machine learning solutions.

### `machine_learning_engineering/sub_agents/initialization/agent.py`

This file defines the initialization agent, which is responsible for setting up the machine learning task and generating a set of initial solutions.

**Functionality:**

- **Task Preparation:**
    - `prepare_task`: Initializes the agent's state with the configuration from `config.py`, sets the random seed for reproducibility, and loads the task description.
    - `create_workspace`: Creates a dedicated workspace for each initial solution, including subdirectories for input data and model candidates.
- **Task Summarization:**
    - `task_summarization_agent`: An agent that summarizes the task description to provide a concise overview for the other agents.
- **Parallel Solution Generation:**
    - `init_parallel_agent`: A `ParallelAgent` that generates multiple initial solutions concurrently. Each parallel branch executes a `SequentialAgent` (`init_solution_gen_agent`) that performs the following steps:
        1.  **Model Retrieval:** Retrieves a list of candidate models suitable for the task.
        2.  **Model Evaluation:** For each candidate model, it generates and executes a Python script to evaluate its performance.
        3.  **Solution Ranking:** Ranks the generated solutions based on their performance scores.
        4.  **Solution Merging:** Merges the solutions to create a more robust solution.
        5.  **Best Solution Selection:** Selects the best-performing solution.
        6.  **Data Usage Check (Optional):** Checks if the solution uses all the provided data.
- **Self-healing:** The model evaluation and merging steps are performed by `run_and_debug_agent` instances, which means that any bugs in the generated code will be automatically fixed.

**Architecture:**

The initialization agent is a `SequentialAgent` that orchestrates the initial phase of the machine learning pipeline. It uses a `ParallelAgent` to efficiently explore different modeling approaches and generate a diverse set of initial solutions. This parallel and self-healing approach allows the system to robustly generate high-quality initial solutions for a given machine learning task.

### `machine_learning_engineering/sub_agents/initialization/prompt.py`

This file defines the prompts used by the initialization agent and its sub-agents.

**Prompts:**

- **`SUMMARIZATION_AGENT_INSTR`**: This prompt is used to instruct a large language model to summarize the task description. The summary is then used to retrieve relevant models.
- **`MODEL_RETRIEVAL_INSTR`**: This prompt instructs the language model to retrieve a list of recent and effective models for the given task, along with example code. The expected output is a JSON object.
- **`MODEL_EVAL_INSTR`**: This prompt instructs the language model to generate a Python script to evaluate a given model on the task. It specifies the output format, including the need to print the final validation performance.
- **`BUG_SUMMARY_INSTR` and `BUG_REFINE_INSTR`**: These are the prompts used for debugging the generated code, similar to the ones in `debug_prompt.py`.
- **`CODE_INTEGRATION_INSTR`**: This prompt instructs the language model to integrate a reference solution into a base solution, with the goal of combining the strengths of both.
- **`CHECK_DATA_USE_INSTR`**: This prompt instructs the language model to check if the generated code uses all the provided data and to modify it if necessary.

These prompts guide the initialization agent through the complex process of generating and evaluating multiple initial solutions for the given machine learning task.

### `machine_learning_engineering/sub_agents/refinement/agent.py`

This file defines the refinement agent, which is responsible for improving the initial solutions generated by the initialization agent.

**Functionality:**

- **Parallel Refinement:** The refinement agent is a `ParallelAgent` that refines multiple solutions concurrently. Each solution is refined in its own parallel branch.
- **Iterative Improvement:** Each parallel branch consists of a `LoopAgent` (`ablation_and_refine_loop_agent`) that iteratively improves the solution over multiple rounds.
- **Ablation Studies:** In each round, the agent first performs an ablation study on the current solution to identify the most important parts of the code.
- **Plan-based Refinement:** Based on the results of the ablation study, the agent generates a plan to refine the code.
- **Implementation and Debugging:** The agent then implements the refinement plan, and if the new code has any bugs, it automatically debugs them.
- **Inner and Outer Loops:** The refinement process consists of an outer loop for the ablation studies and an inner loop for refining the plan and implementation.
- **State Management:** The agent uses a set of callback functions to manage the state of the refinement process, including the current refinement step, the plans, and the performance of the different solutions.
- **Dynamic Prompt Generation:** The prompts for the refinement agents are generated dynamically based on the current state of the refinement process.

**Architecture:**

The refinement agent is a key component of the system's ability to generate high-quality solutions. By using a combination of ablation studies, plan-based refinement, and automated debugging, the agent can systematically improve the initial solutions and converge on a high-performing solution. The use of parallel and nested loops allows for a thorough and efficient exploration of the solution space.

### `machine_learning_engineering/sub_agents/submission/agent.py`

This file defines the submission agent, which is responsible for generating the final submission file for the machine learning competition.

**Functionality:**

The submission agent is a `run_and_debug_agent` from `debug_util.py`. Its main purpose is to take the best-performing solution generated by the previous agents and modify it to produce a `submission.csv` file in the correct format.

*   **Selects the best solution:** The `get_submission_and_debug_agent_instruction` function selects the best solution from all the solutions generated during the initialization, refinement, and ensembling phases, based on their validation scores.
*   **Generates submission code:** It then uses the `ADD_TEST_FINAL_INSTR` prompt (from `submission/prompt.py`) to instruct a large language model to add the necessary code to the best solution to make predictions on the test set and generate the submission file.
*   **Handles final execution:** The `check_submission_finish` callback ensures that the submission code is only generated once.
*   **Self-healing:** Since it's a `run_and_debug_agent`, if the generated submission script has any bugs, the agent will automatically try to fix them.

**Architecture:**

The submission agent is the final step in the machine learning pipeline. It takes the best solution and adapts it to produce the final output for the competition. By using a `run_and_debug_agent`, it ensures that the final submission script is robust and error-free.

### `machine_learning_engineering/sub_agents/submission/prompt.py`

This file defines the prompt that guides the submission agent in generating the final submission file.

**Functionality:**

The functionality is defined by the `ADD_TEST_FINAL_INSTR` prompt, which instructs a large language model to modify a given Python solution to produce a submission file.

*   **`ADD_TEST_FINAL_INSTR`**: This prompt provides the LLM with the task description and the best Python solution found so far. It instructs the LLM to add code to:
    *   Load the test data from the `./input` directory.
    *   Make predictions on the test data using the trained model.
    *   Save the predictions to a `submission.csv` file in the `./final` directory.
    *   The prompt also specifies that the solution should not be modified too much, and that the output should be a single, self-contained Python script.

**Prompts Source:**

```python
"""Defines the prompts for the submission agent."""


ADD_TEST_FINAL_INSTR = """# Introduction
- You are a Kaggle grandmaster attending a competition.
- In order to win this competition, you need to come up with an excellent solution in Python.
- We will now provide a task description and a Python solution.
- What you have to do on the solution is just loading test samples and create a submission file.

# Task description
{task_description}

# Python solution
```python
{code}
```

# Your task
- Load the test samples and create a submission file.
- All the provided data is already prepared and available in the `./input` directory. There is no need to unzip any files.
- Test data is available in the `./input` directory.
- Save the test predictions in a `submission.csv` file. Put the `submission.csv` into `./final` directory.
- You should not drop any test samples. Predict the target value for all test samples.
- This is a very easy task because the only thing to do is to load test samples and then replace the validation samples with the test samples. Then you can even use the full training set!

# Required
- Do not modify the given Python solution code too much. Try to integarte test submission with minimal changes.
- There should be no additional headings or text in your response.
- The code should be a single-file Python program that is self-contained and can be executed as-is.
- Your response should only contain a single code block.
- Do not forget the ./final/submission.csv file.
- Do not use exit() function in the Python code.
- Do not use try: and except: or if else to ignore unintended behavior."""
```

### `tests/test_agents.py`

This file contains test cases for the Machine Learning Engineering agent.

**Functionality:**

The file defines a single test case, `test_happy_path`, which is designed to be run with `pytest`.

*   **Test Setup:**
    *   The test uses `dotenv` to load environment variables.
    *   It uses the Google ADK's `InMemoryRunner`, `InMemorySessionService`, and `InMemoryArtifactService` to run the agent in a test environment without any external dependencies.
*   **Test Logic:**
    *   The `test_happy_path` function sends a simple question ("who are you") to the `root_agent`.
    *   It then streams the response from the agent and asserts that the response contains the words "machine learning".
*   **Purpose:** This test serves as a basic sanity check to ensure that the `root_agent` is correctly initialized and can respond to simple inputs.

**Test Source:**

```python
"""Test cases for the Machine Learning Engineering agent and its sub-agents."""


import dotenv
import os
import sys
import pytest
import textwrap
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google.genai import types
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService

from machine_learning_engineering.agent import root_agent

session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_happy_path():
    """Runs the agent on a simple input and expects a normal response."""
    user_input = textwrap.dedent(
        """
        Question: who are you
        Answer: Hello! I am a Machine Learning Engineering Agent.
    """
    ).strip()

    app_name = "machine-learning-engineering"

    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = types.Content(parts=[types.Part(text=user_input)], role="user")
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        print(event)
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    # The correct answer should mention 'machine learning'.
    assert "machine learning" in response.lower()

if __name__ == "__main__":
    unittest.main()
```

### `machine_learning_engineering/sub_agents/refinement/prompt.py`

This file defines the prompts that guide the refinement agent in improving the generated machine learning solutions. These prompts are designed to be used with a large language model to perform ablation studies, generate refinement plans, and implement those plans.

**Functionality:**

The functionality is defined by a set of prompts, each serving a specific purpose in the refinement process.

*   **Ablation Study Prompts:**
    *   `ABLATION_INSTR`: This prompt instructs the LLM to generate a Python script to perform an ablation study on a given solution. The goal is to identify which parts of the code contribute most to the performance. The LLM is expected to generate a script that modifies or disables parts of the training process and measures the impact on performance.
    *   `ABLATION_SEQ_INSTR`: A sequential version of the ablation prompt, used when previous ablation studies have already been performed. It instructs the LLM to focus on parts of the code that have not been previously considered.

*   **Ablation Summary Prompt:**
    *   `SUMMARIZE_ABLATION_INSTR`: This prompt instructs the LLM to summarize the results of an ablation study, given the code for the study and the printed output.

*   **Refinement Planning Prompts:**
    *   `EXTRACT_BLOCK_AND_PLAN_INSTR`: This prompt instructs the LLM to analyze the results of an ablation study and propose a plan to improve the solution. It also asks the LLM to extract the specific code block that needs to be modified. The expected output is a JSON object containing the plan and the code block.
    *   `EXTRACT_BLOCK_AND_PLAN_SEQ_INSTR`: A sequential version of the planning prompt, used when previous refinement attempts have been made. It instructs the LLM to focus on parts of the code that have not been improved before.
    *   `PLAN_REFINEMENT_INSTR`: This prompt instructs the LLM to refine an existing improvement plan, based on the performance of previous attempts.

*   **Plan Implementation Prompt:**
    *   `IMPLEMENT_PLAN_INSTR`: This prompt instructs the LLM to implement a given improvement plan on a specific code block. The expected output is a single markdown code block with the improved code.

**Prompts Source:**

```python
"""Defines the prompts for the refinement agent."""

ABLATION_INSTR = """# Introduction
- You are a Kaggle grandmaster attending a competition.
- In order to win this competition, you need to perform an ablation study on the current Python solution to know which parts of the code contribute the most to the overall performance.
- We will now provide a current Python solution.

# Python solution
```python
{code}
```
# Instructions
- You need to generate a simple Python code that performs an ablation study on the above Python solution script.
- The generated code should create variations by modifying or disabling parts (1-2 simple parts) of the training process.
- For each ablation, print out how the modification affects the model's performance.

# Response format
- There should be no additional headings or text in your response.
- The Python code for the ablation study should not load test data. It should only focus on training and evaluating the model on the validation set.
- The code should include a printing statement that shows the performance of each ablation.
- The code should consequently print out which part of the code contributes the most to the overall performance.
"""

ABLATION_SEQ_INSTR = """# Introduction
- You are a Kaggle grandmaster attending a competition.
- In order to win this competition, you need to perform an ablation study on the current Python solution to know which parts of the code contribute the most to the overall performance.
- We will now provide a current Python solution.
- We will also provide the summaries of previous ablation studies.

# Python solution
```python
{code}
```

{prev_ablations}

# Instructions
- You need you to generate a simple Python code that performs an ablation study on the train.py script.
- The generated code should create variations by modifying or disabling parts (2-3 parts) of the training process.
- Your ablation study should concentrate on the other parts that have not been previously considered.
- For each ablation, print out how the modification affects the model's performance.

# Response format
- There should be no additional headings or text in your response.
- The Python code for the ablation study should not load test data. It should only focus on training and evaluating the model on the validation set.
- The code should include a printing statement that shows the performance of each ablation.
- The code should consequently print out what part of the code contributes the most to the overall performance.
"""

SUMMARIZE_ABLATION_INSTR = """# Your code for ablation study was:
```python
{code}
```

# Ablation study results after running the above code:
{result}

# Your task
- Summarize the result of ablation study based on the code and printed output.
"""

EXTRACT_BLOCK_AND_PLAN_INSTR = """# Introduction
- You are a Kaggle grandmaster attending a competition.
- In order to win this competition, you need to extract a code block from the current Python solution and improve the extracted block for better performance.
- Your suggestion should be based on the ablation study results of the current Python solution.
- We will now provide the current Python solution and the ablation study results.

# Python solution
```python
{code}
```

# Ablation study results
{ablation_results}

# Your task
- Given the ablation study results, suggest an effective next plan to improve the above Python script.
- The plan should be a brief outline/sketch of your proposed solution in natural language (3-5 sentences).
- Please avoid plan which can make the solution's running time too long (e.g., searching hyperparameters in a very large search space).
- Also extract the code block from the above Python script that need to be improved according to the proposed plan.

# Response format
- Your response should be a brief outline/sketch of your proposed solution in natural language (3-5 sentences) and a single markdown code block which is the code block that need to be improved.
- The code block can be long but should be exactly extracted from the Python script provided above.

Use this JSON schema:

Refine_Plan = {{'code_block': str, 'plan': str}}
Return: list[Refine_Plan]"""

EXTRACT_BLOCK_AND_PLAN_SEQ_INSTR = """# Introduction
- You are a Kaggle grandmaster attending a competition.
- In order to win this competition, you need to extract a code block from the current Python solution and improve the extracted block for better performance.
- Your suggestion should be based on the ablation study results of the current Python solution.
- We will now provide the current Python solution and the ablation study results.
- We also provide code blocks which you have tried to improve previously.

# Python solution
```python
{code}
```

# Ablation study results
{ablation_results}

{prev_code_blocks}

# Your task
- Given the ablation study results, suggest an effective next plan to improve the above Python script.
- The plan should be a brief outline/sketch of your proposed solution in natural language (3-5 sentences).
- Please avoid plan which can make the solution's running time too long (e.g., searching hyperparameters in a very large search space).
- Try to improve the other part which was not considered before.
- Also extract the code block from the above Python script that need to be improved according to the proposed plan. You should try to extract the code block which was not improved before.

# Response format
- Your response should be a brief outline/sketch of your proposed solution in natural language (3-5 sentences) and a single markdown code block which is the code block that need to be improved.
- The code block can be long but should be exactly extracted from the Python script provided above.

Use this JSON schema:

Refine_Plan = {{'code_block': str, 'plan': str}}
Return: list[Refine_Plan]"""

PLAN_REFINEMENT_INSTR = """# Introduction
- You are a Kaggle grandmaster attending a competition.
- In order to win this competition, you have to improve the code block for better performance.
- We will provide the code block you are improving and the improvement plans you have tried.

# Code block
```python
{code_block}
```

# Improvement plans you have tried

{prev_plan_summary}

# Your task
- Suggest a better plan to improve the above code block.
- The suggested plan must be novel and effective.
- Please avoid plans which can make the solution's running time too long (e.g., searching hyperparameters in a very large search space).
- The suggested plan should be differ from the previous plans you have tried and should receive a higher score.

# Response format
- Your response should be a brief outline/sketch of your proposed solution in natural language (3-5 sentences).
- There should be no additional headings or text in your response.
"""

IMPLEMENT_PLAN_INSTR = """# Introduction
- You are a Kaggle grandmaster attending a competition.
- In order to win this competition, you need refine the code block for better performance based on the improvement plan.
- We will now provide the code block and the improvement plan.

# Code block
```python
{code_block}
```

# Improvement plan
{plan}

# Your task
- Implement the improvement plan on the above code block. But do not remove subsampling if exists.
- The code block should be improved according to the proposed plan.
- Note that all the variable including actual data is defined earlier (since you are just seeing a code block), therefore do not introduce dummy variables.

# Response format
- Your response should be a single markdown code block (wrapped in ```) which is the improved code block.
- There should be no additional headings or text in your response.
"""
```
