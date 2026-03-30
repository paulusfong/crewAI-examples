# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of **complete CrewAI applications** demonstrating end-to-end implementations using the CrewAI framework (v0.152.0) for orchestrating AI agents. The repository contains three main types of examples:

- **Crews** (`/crews`) - Traditional multi-agent implementations using the CrewAI framework
- **Flows** (`/flows`) - Advanced orchestration using CrewAI Flows with state management and complex workflows
- **Integrations** (`/integrations`) - Examples showing CrewAI integration with other platforms (LangGraph, Azure, NVIDIA)
- **Notebooks** (`/notebooks`) - Jupyter notebooks for interactive exploration

## Dependency Management

**All examples use UV for package management**, not Poetry or pip directly.

### Common Commands

```bash
# Install dependencies and create virtual environment
uv sync

# Run a specific example (if it has a script defined)
uv run <script_name>  # e.g., uv run stock_analysis

# Train a crew (for examples with training capability)
uv run train <iterations>
```

## Project Structure Patterns

### Standard Crew Structure

Most crew examples follow this layout:

```
example_name/
├── pyproject.toml           # Dependencies and entry point scripts
├── uv.lock                  # Locked dependencies
├── .env.example             # Example environment variables
├── src/
│   └── example_name/
│       ├── main.py          # Entry point with run() and train() functions
│       ├── crew.py          # Main crew class with @CrewBase decorator
│       ├── config/
│       │   ├── agents.yaml  # Agent definitions (role, goal, backstory)
│       │   └── tasks.yaml   # Task definitions (description, expected_output)
│       └── tools/           # Custom tool implementations
│           └── custom_tool.py
```

### Legacy/Simple Structure

Some examples (like `starter_template`) use a simpler structure:

```
example_name/
├── main.py       # Main crew logic
├── agents.py     # Agent definitions (Python classes)
├── tasks.py      # Task definitions (Python classes)
└── .env_example
```

## CrewAI Architecture Patterns

### The @CrewBase Pattern (Modern Approach)

The modern pattern uses the `@CrewBase` decorator with method decorators:

```python
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MyCrewClass:
    agents_config = 'config/agents.yaml'  # Path to YAML config
    tasks_config = 'config/tasks.yaml'

    @agent
    def my_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_name'],
            tools=[...],
            llm=llm
        )

    @task
    def my_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_name'],
            agent=self.my_agent()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Auto-populated from @agent methods
            tasks=self.tasks,    # Auto-populated from @task methods
            process=Process.sequential,
            verbose=True
        )
```

**Key Points:**
- The `@agent` and `@task` decorators automatically collect methods into `self.agents` and `self.tasks` lists
- YAML configs define agent properties (role, goal, backstory) and task properties (description, expected_output)
- The `config=` parameter loads from YAML using the key name (e.g., `agents.yaml['agent_name']`)

### YAML Configuration Files

Agent config (`config/agents.yaml`):
```yaml
agent_name:
  role: >
    Agent's role description
  goal: >
    What the agent aims to achieve
  backstory: >
    Agent's background and expertise
```

Task config (`config/tasks.yaml`):
```yaml
task_name:
  description: >
    Detailed task description
  expected_output: >
    What output format/content is expected
```

### Custom Tools

Custom tools are typically placed in a `tools/` directory and inherit from CrewAI's base tool classes:

```python
from crewai_tools import BaseTool

class CustomTool(BaseTool):
    name: str = "Tool Name"
    description: str = "What the tool does"

    def _run(self, argument: str) -> str:
        # Tool implementation
        return result
```

Tools are passed to agents in the `tools=[...]` parameter.

### Entry Points

The `main.py` typically defines:
- `run()` - Execute the crew with inputs
- `train()` - Train the crew for N iterations (optional)

These are registered as scripts in `pyproject.toml`:
```toml
[project.scripts]
example_name = "example_name.main:run"
train = "example_name.main:train"
```

## CrewAI Flows

Flows are located in `/flows` and represent more complex orchestration patterns:

- **State Management** - Flows maintain state across execution steps
- **Conditional Routing** - Decision logic based on previous results
- **Parallel Execution** - Multiple crews running simultaneously
- **Human-in-the-Loop** - Workflows that pause for human input
- **Multi-Crew Orchestration** - Coordinating multiple specialized crews

Flow examples use different patterns than standard crews and should be studied individually based on the use case.

## LLM Configuration

Examples use different LLM providers:

**OpenAI (most common):**
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
```

**Local models (Ollama):**
```python
from langchain.llms import Ollama
llm = Ollama(model="llama3.1")
```

**Environment variables** typically required:
- `OPENAI_API_KEY`
- `OPENAI_ORGANIZATION` (optional)
- Other API keys depending on tools used (e.g., `SEC_API_API_KEY`, `SERPER_API_KEY`)

## Working with Examples

### To Run an Example:

1. Navigate to the example directory: `cd crews/example_name` or `cd flows/example_name`
2. Copy environment file: `cp .env.example .env` (then add your API keys)
3. Install dependencies: `uv sync`
4. Run the example: `uv run example_name` (or `python main.py` for simple examples)

### To Modify an Example:

- **Change agent behavior**: Edit `config/agents.yaml` to modify role, goal, or backstory
- **Change tasks**: Edit `config/tasks.yaml` to modify task descriptions or expected outputs
- **Add tools**: Create new tool classes in `tools/` directory and add to agent's `tools=[...]` list
- **Change LLM**: Modify the `llm=` parameter in agent creation
- **Add agents/tasks**: Add new `@agent` or `@task` methods to the crew class

## Training Crews

Some examples support training (fine-tuning agents based on feedback):

```bash
uv run train 5  # Train for 5 iterations
```

Training data is stored in `trained_agents_data.pkl` after training.

## Common Integration Patterns

- **SEC API Integration** - See `stock_analysis` for SEC 10-K/10-Q filings
- **Web Scraping** - Many examples use `ScrapeWebsiteTool` and `WebsiteSearchTool`
- **Search** - DuckDuckGo search is commonly used via `DuckDuckGoSearchRun()`
- **File Processing** - Examples like `meta_quest_knowledge` show PDF/document Q&A patterns
- **External APIs** - Examples demonstrate Trello, Slack, Gmail integrations

## Testing and Quality Assurance

### Stock Analysis Example - Mutation Testing Setup

The `crews/stock_analysis` example includes a comprehensive test suite demonstrating testing best practices:

**Test Infrastructure:**
- `tests/tools/test_calculator_tool.py` - 28 comprehensive test cases
- 85% code coverage on CalculatorTool
- Mutation testing configuration (pytest + mutmut)

**Running Tests:**
```bash
cd crews/stock_analysis

# Run tests
python3 -m pytest tests/ -v

# With coverage report
python3 -m pytest tests/ --cov=src/stock_analysis/tools --cov-report=html

# View coverage
open htmlcov/index.html
```

**Test Organization:**
- Basic operations (6 tests)
- Complex expressions (4 tests)
- Unary operators (3 tests)
- Error handling (8 tests)
- Edge cases (5 tests)
- Real-world examples (2 tests)

See `MUTATION_TESTING_SUMMARY.md` in stock_analysis for detailed documentation on mutation testing concepts and test quality evaluation.

## Important Notes

- **CrewAI Version**: All examples use CrewAI >=0.152.0
- **Python Version**: Most require Python >=3.10, <=3.13 (some require >=3.12)
- **Process Types**: Crews can use `Process.sequential` (default) or `Process.hierarchical`
- **Delegation**: Agents can have `allow_delegation=True/False` to enable/disable task delegation
- **Verbosity**: Set `verbose=True` in Crew or Agent for detailed logging
