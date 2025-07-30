# Agent Evaluator

A lightweight utility for comparing agents or models using datasets, with support for model, agent, and dataset evaluation modes. Built on top of `opik`, `google-adk`, and related libraries.

## Features

- Compare LLM agents or models on custom datasets
- Evaluate agent performance, answer relevance, hallucination, and more
- Flexible configuration via JSON files
- CLI interface for easy usage

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd agent_evaluator
   ```

2. **Install dependencies:**
   - Using pip (recommended for most users):
     ```bash
     pip install .
     ```
   - Or, using the included `pyproject.toml`:
     ```bash
     pip install .
     ```

   > **Note:** You may want to use a virtual environment:
   > ```bash
   > python -m venv .venv
   > source .venv/bin/activate
   > ```

## Configuration

1. **Create a configuration file:**
   - Copy `config_template.json` to `config.json` and edit as needed:
     ```bash
     cp config_template.json config.json
     ```
   - Fill in the required fields for your agents, models, datasets, and judge model.

2. **Prepare your agent and dataset files:**
   - Implement your agent(s) in a Python file (e.g., `agent.py`).
   - Prepare your dataset(s) in JSONL format, where each line is a JSON object with at least a `user_question` field.

## Usage

Run the evaluator in one of three modes: `model`, `agent`, or `dataset`.

```bash
python agent_evaluator/evaluator.py <mode>
```

Where `<mode>` is one of:
- `model` &mdash; Compare different models using a single agent and dataset.
- `agent` &mdash; Compare different agents on the same dataset.
- `dataset` &mdash; Compare different datasets using a single agent.

**Example:**
```bash
python agent_evaluator/evaluator.py model
```

## Configuration Example

Here is a sample `config.json` structure:

```json
{
  "model_comparison": {
    "delay_seconds": 0.0,
    "baseline_model": "your_baseline_model_name",
    "candidate_models": ["your_candidate_model_name"],
    "agent": {
      "class_name": "YourAgentClass",
      "module_path": "path/to/your/agent.py"
    },
    "dataset": "path/to/your/dataset.jsonl",
    "judge_model": "your_judge_model_name"
  },
  "agent_comparison": {
    "delay_seconds": 0.0,
    "baseline_agent": {
      "name": "your_baseline_agent_name",
      "module_path": "path/to/your/agent.py"
    },
    "candidate_agents": [
      {
        "name": "your_candidate_agent_name",
        "module_path": "path/to/your/agent.py"
      }
    ],
    "dataset": "path/to/your/dataset.jsonl",
    "judge_model": "your_judge_model_name"
  },
  "dataset_comparison": {
    "baseline_dataset": "path/to/your/baseline_dataset.jsonl",
    "candidate_datasets": ["path/to/your/candidate_dataset.jsonl"],
    "agent": {
      "name": "your_agent_name",
      "module_path": "path/to/your/agent.py"
    },
    "judge_model": "your_judge_model_name"
  }
}
```

## Notes

- Make sure your agent and judge model implementations are accessible via the paths specified in the config.
- Datasets should be in JSONL format, with each line containing at least a `user_question` field.
- For advanced usage, see the docstrings in `agent_evaluator/evaluator.py`. 