#!/usr/bin/env python3
"""Lightweight agent / model comparison utility."""

import json
import sys
import os
import importlib.util

# Add project root to the Python path to allow running as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Unconditionally disable OpenTelemetry automatic instrumentation.
# This prevents connection errors if an OTLP collector is not running.
# The manual opik.trace() calls will still function correctly.
os.environ["OTEL_SDK_DISABLED"] = "true"

import asyncio
from typing import Dict, Any, Tuple
from google.genai import types
import opik
import copy
import numpy as np

from scipy.spatial.distance import pdist, squareform
from sentence_transformers import SentenceTransformer
from google.adk.agents import Agent
from src import agent as agent_definitions
from src.opik_setup import setup_opik_tracing

# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------

try:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except ImportError:
    # Either python-dotenv is missing or an unexpected error occurred. We simply
    # continue and rely on the variable being set in the environment.
    pass


class AgentEvaluator:
    """Compare agents or models against datasets defined in a JSON config."""

    def __init__(self, config_file: str = "config.json"):
        """Initialize with path to JSON config file."""
        self.config = self._load_config(config_file)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    
    async def _call_agent(self, runner, user_question: str, session_id: str, delay_seconds: float = 0.0):
        """Call agent and return response."""
        if delay_seconds > 0:
            print(f"--- Throttling: Waiting {delay_seconds} seconds before request ---")
            await asyncio.sleep(delay_seconds)
        
        content = types.Content(role='user', parts=[types.Part(text=user_question)])
        
        response = None
        try:
            async for event in runner.run_async(user_id="eval_user", session_id=session_id, new_message=content):
                if event.is_final_response():
                    if event.content and event.content.parts and len(event.content.parts) > 0:
                        response = event.content.parts[0].text
                    elif event.actions and event.actions.escalate:
                        response = f"Agent escalated: {event.error_message or 'No message'}"
        except Exception as e:
            return f"Error calling agent: {str(e)}"
        
        return response or "No response"

    async def _setup_session(self, session_service, app_name: str, session_id: str):
        """Setup evaluation session with cleanup."""
        await session_service.delete_session(app_name=app_name, user_id="eval_user", session_id=session_id)
        await session_service.create_session(app_name=app_name, user_id="eval_user", session_id=session_id, state={})

    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Configuration file not found at '{config_file}'")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid JSON in configuration file at '{config_file}'")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Unexpected error loading configuration file '{config_file}': {e}")
            sys.exit(1)

    def _import_agent_module(self, agent_module_path: str):
        """Dynamically import agent module"""
        spec = importlib.util.spec_from_file_location("agent_module", agent_module_path)
        if spec is None or spec.loader is None:
            print(f"ERROR: Could not create module spec from '{agent_module_path}'")
            sys.exit(1)
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        return agent_module

    def _create_agent_from_config(self, agent_config: Dict, model=None):
        """Create agent from configuration"""
        # Import the agent module
        agent_module = self._import_agent_module(agent_config["module_path"])

        # Get the agent class from the module
        agent_class = getattr(agent_module, agent_config["class_name"])

        # Create a copy of the agent to avoid modifying the original
        agent = copy.deepcopy(agent_class)

        # Create agent with specified model (if provided)
        if model:
            agent.model = model
        
        return agent

    def _get_agent_from_config(self, agent_config: Dict):
        """Dynamically load an agent variable from a module and return a copy."""
        module_path = agent_config["module_path"]
        agent_name = agent_config["name"]
        
        # Re-use the agent module if already imported
        agent_module = self._import_agent_module(module_path)
        agent_variable = getattr(agent_module, agent_name)
        return copy.deepcopy(agent_variable)

    def _get_model_from_config(self, model_config: Dict):
        """Return model string or predefined object based on config entry"""
        name = model_config["name"]

        # If the model is a dictionary, it's a pre-configured LiteLLM model
        if isinstance(model_config, dict):
            name = model_config["name"]
            if name == "gpt_llm":
                return agent_definitions.gpt_llm
            elif name == "claude_llm":
                return agent_definitions.claude_llm

        # Otherwise, treat the name as the raw model identifier string (Gemini etc.)
        return name

    async def _get_pairwise_judgment(self, judge_runner, question: str, response_a: str, response_b: str, context_prefix: str = "judge") -> Tuple[str, str]:
        """Get a pairwise judgment from a judge model."""
        prompt = f"""[Question]
{question}

[Response A]
{response_a}

[Response B]
{response_b}

[Instructions]
You are a helpful and harmless AI assistant. Your task is to evaluate the quality of two responses (A and B) to the user's question.
Consider correctness, completeness, and helpfulness.
Respond ONLY with a valid JSON object, and do NOT include any extra text, markdown, or code fences. Your entire response must be a single line of JSON, like: {{\"verdict\": \"A\", \"reasoning\": \"your explanation here\"}}
"""

        session_id = f"{context_prefix}_session"
        await self._setup_session(judge_runner.session_service, "judge_app", session_id)
        
        verdict_text = await self._call_agent(judge_runner, prompt, session_id)

        # Parse verdict
        verdict = "TIE" # default
        reasoning = "No reasoning provided."

        if verdict_text:
            parsed = json.loads(verdict_text)
            verdict = parsed.get("verdict", "TIE")
            reasoning = parsed.get("reasoning", "No reasoning provided.")

        return verdict, reasoning

    async def _get_complexity_judgment(self, judge_runner, question: str, context_prefix: str = "complexity_judge") -> int:
        """Get a complexity judgment from a judge model."""
        prompt = f"""[Question]
{question}

[Instructions]
You are a helpful and harmless AI assistant. Your task is to evaluate the complexity of the user's question.
Rate the complexity on a scale from 1 to 5, where 1 is very simple and 5 is very complex.
Your decision must be a single number on the first line, enclosed in double square brackets. For example: [[3]]."""

        session_id = f"{context_prefix}_session"
        await self._setup_session(judge_runner.session_service, "judge_app", session_id)
        
        response_text = await self._call_agent(judge_runner, prompt, session_id)

        try:
            return int(response_text.strip().replace("[[", "").replace("]]", ""))
        except (ValueError, TypeError):
            return 0 # Default to 0 if parsing fails

    def _calculate_semantic_diversity(self, questions: list[str], model) -> float:
        """Calculate semantic diversity of questions."""
        if len(questions) < 2:
            return 0.0
        embeddings = model.encode(questions)
        # Calculate pairwise cosine distances, and take the mean
        distance_matrix = pdist(embeddings, 'cosine')
        return np.mean(distance_matrix)

    def _calculate_redundancy(self, questions: list[str], model, threshold=0.95) -> float:
        """Calculate the percentage of redundant questions."""
        if len(questions) < 2:
            return 0.0
        embeddings = model.encode(questions)
        # Calculate pairwise cosine similarities
        similarity_matrix = 1 - squareform(pdist(embeddings, 'cosine'))
        # Find pairs with similarity > threshold (excluding self-similarity)
        redundant_pairs = np.sum(np.triu(similarity_matrix, k=1) > threshold)
        return (redundant_pairs / (len(questions) * (len(questions) - 1) / 2)) * 100

    async def _analyze_single_dataset(
        self, dataset_path: str, runner, judge_runner, embedding_model, opik_client
    ) -> Dict:
        """Analyzes a single dataset and returns a dictionary of quality metrics."""
        with open(dataset_path, 'r') as f:
            dataset = [json.loads(line) for line in f]
        
        questions = [ex.get("user_question", "") for ex in dataset]
        num_examples = len(questions)
        print(f"Found {num_examples} examples.")

        # 1. Agent Performance (Difficulty)
        success_count = 0
        for i, example in enumerate(dataset, 1):
            session_id = f"dataset_comparison_{os.path.basename(dataset_path)}_example_{i}"
            await self._setup_session(runner.session_service, runner.app_name, session_id)
            response = await self._call_agent(runner, example["user_question"], session_id)
            if not response.startswith("Error") and not response.startswith("Agent escalated"):
                success_count += 1
        
        agent_performance = (success_count / num_examples) * 100 if num_examples > 0 else 0
        print(f"  - Agent Performance (Success Rate): {agent_performance:.2f}%")

        # 2. Complexity Analysis
        complexities = []
        for i, q in enumerate(questions, 1):
            context = f"dataset_comparison_{os.path.basename(dataset_path)}_complexity_example_{i}"
            complexities.append(await self._get_complexity_judgment(judge_runner, q, context_prefix=context))
        avg_complexity = np.mean(complexities) if complexities else 0
        print(f"  - Average Complexity (1-5): {avg_complexity:.2f}")

        # 3. Semantic Diversity
        diversity_score = self._calculate_semantic_diversity(questions, embedding_model)
        print(f"  - Semantic Diversity Score: {diversity_score:.4f}")

        # 4. Redundancy Check
        redundancy_score = self._calculate_redundancy(questions, embedding_model)
        print(f"  - Redundancy Score (% near-duplicates): {redundancy_score:.2f}%")

        dataset_results = {
            "agent_performance_success_rate": agent_performance,
            "average_complexity": avg_complexity,
            "semantic_diversity_score": diversity_score,
            "redundancy_percentage": redundancy_score,
            "total_examples": num_examples
        }

        opik_client.trace(
            name=f"dataset_comparison:analysis:{os.path.basename(dataset_path)}",
            input={"dataset_path": dataset_path},
            output=dataset_results
        ).end()

        return dataset_results

    async def compare_models(self) -> Dict:
        """Compare different models using the same agent and dataset"""
        print("🚀 MODEL COMPARISON (Pairwise)")
        config = self.config["model_comparison"]
        
        baseline_model_name = config["baseline_model"]
        judge_model_name = config.get("judge_model", baseline_model_name) # Default to baseline if not set
        
        print(f"Agent: {config['agent']['class_name']} | Dataset: {config['dataset']}")
        print(f"Baseline Model: {baseline_model_name}")
        print(f"Judge Model: {judge_model_name}")

        results = {}

        # Create the agent and model instances
        baseline_model_obj = self._get_model_from_config({"name": baseline_model_name})
        baseline_agent = self._create_agent_from_config(config["agent"], baseline_model_obj)
        setup_opik_tracing(baseline_agent)
        
        session_service = InMemorySessionService()

        judge_model_obj = self._get_model_from_config({"name": judge_model_name})
        judge_agent = Agent(model=judge_model_obj, name="judge_agent", instruction="You are an expert evaluator.")
        judge_runner = Runner(agent=judge_agent, app_name="judge_app", session_service=session_service)

        print("--- Initializing Opik client for tracing ---")
        project_name = os.getenv("OPIK_PROJECT_NAME", "adk-evaluator")
        opik_client = opik.Opik(project_name=project_name)

        for candidate_model_name in config["candidate_models"]:
            comparison_name = f"{baseline_model_name}_vs_{candidate_model_name}"
            print("-" * 60)
            print(f"Comparing: '{baseline_model_name}' (Baseline) vs. '{candidate_model_name}' (Candidate)")
            
            app_name = config["agent"]["class_name"]
            baseline_runner = Runner(agent=baseline_agent, app_name=app_name, session_service=session_service)
            
            candidate_model_obj = self._get_model_from_config({"name": candidate_model_name})
            candidate_agent = self._create_agent_from_config(config["agent"], candidate_model_obj)
            setup_opik_tracing(candidate_agent)
            candidate_runner = Runner(agent=candidate_agent, app_name=app_name, session_service=session_service)

            # Load the dataset
            dataset_path = config["dataset"]
            with open(dataset_path, 'r') as f:
                dataset = [json.loads(line) for line in f]

            print(f"Found {len(dataset)} examples in {dataset_path}")
            
            # Track scores
            scores = {"wins": 0, "losses": 0, "ties": 0}

            for i, example in enumerate(dataset, 1):
                question = example.get("user_question", "")
                print(f"\n--- Example {i} ---")

                # Setup unique sessions for this comparison
                baseline_session_id = f"model_comparison_{comparison_name}_baseline_example_{i}"
                candidate_session_id = f"model_comparison_{comparison_name}_candidate_example_{i}"
                await self._setup_session(session_service, app_name, baseline_session_id)
                await self._setup_session(session_service, app_name, candidate_session_id)
                
                # Get responses from both agents
                delay = self.config.get("model_comparison", {}).get("delay_seconds", 0.0)
                baseline_response = await self._call_agent(baseline_runner, question, baseline_session_id)
                candidate_response = await self._call_agent(candidate_runner, question, candidate_session_id, delay_seconds=delay)
                
                print(f"  - Baseline response: {baseline_response[:50].strip()}...")
                print(f"  - Candidate response: {candidate_response[:50].strip()}...")

                # Get the verdict
                judge_context = f"model_comparison_{comparison_name}_judge_example_{i}"
                verdict, reasoning = await self._get_pairwise_judgment(
                    judge_runner, question, baseline_response, candidate_response, context_prefix=judge_context
                )
                
                trace_name = f"model_comparison:{comparison_name}:example_{i}"
                trace = opik_client.trace(
                    name=trace_name,
                    input={"question": question, "baseline": baseline_response, "candidate": candidate_response},
                    output={"verdict": verdict, "reasoning": reasoning}
                )
                trace.end()
                
                print(f"  - Verdict: {verdict}")
                print(f"  - Reasoning: {reasoning}")

                if verdict == "A":
                    scores["wins"] += 1
                elif verdict == "B":
                    scores["losses"] += 1
                elif verdict == "TIE":
                    scores["ties"] += 1

            # Store and print results for this comparison
            print("\n" + "=" * 60)
            print(f"FINAL SCORE for {comparison_name}:")
            print(f"Baseline ({baseline_model_name}) Wins: {scores['wins']}/{len(dataset)}")
            print(f"Candidate ({candidate_model_name}) Wins: {scores['losses']}/{len(dataset)}")
            print(f"Ties: {scores['ties']}/{len(dataset)}")
            print("=" * 60)

            results[comparison_name] = {
                "baseline_wins": scores["wins"],
                "candidate_wins": scores['losses'],
                "ties": scores['ties'],
                "total": len(dataset)
            }
        
        return results

    async def compare_datasets(self) -> Dict:
        """Compare a baseline dataset against candidate datasets."""
        print("🚀 DATASET COMPARISON (Pairwise)")
        config = self.config["dataset_comparison"]
        
        agent_config = config["agent"]
        judge_model_name = config["judge_model"]
        
        print(f"Agent: {agent_config['name']}")
        print(f"Judge Model: {judge_model_name}")

        results = {}

        # Initial Setup
        print("--- Initializing services and agent ---")
        project_name = os.getenv("OPIK_PROJECT_NAME", "adk-evaluator")
        opik_client = opik.Opik(project_name=project_name)
        session_service = InMemorySessionService()
        judge_model_obj = self._get_model_from_config({"name": judge_model_name})
        judge_agent = Agent(model=judge_model_obj, name="judge_agent", instruction="You are an expert evaluator.")
        judge_runner = Runner(agent=judge_agent, app_name="judge_app", session_service=session_service)
        agent_to_test = self._get_agent_from_config(agent_config)
        setup_opik_tracing(agent_to_test)
        runner = Runner(agent=agent_to_test, app_name=f"app_{agent_config['name']}", session_service=session_service)
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Analyze Baseline Dataset
        baseline_dataset_path = config["baseline_dataset"]
        print("-" * 60)
        print(f"Analyzing Baseline Dataset: {baseline_dataset_path}")
        baseline_results = await self._analyze_single_dataset(
            baseline_dataset_path, runner, judge_runner, embedding_model, opik_client
        )
        results["baseline"] = {"path": baseline_dataset_path, "metrics": baseline_results}

        # Compare against each Candidate Dataset
        for candidate_dataset_path in config.get("candidate_datasets", []):
            comparison_name = f"{os.path.basename(baseline_dataset_path)}_vs_{os.path.basename(candidate_dataset_path)}"
            print("\n" + "=" * 60)
            print(f"Comparing: '{os.path.basename(baseline_dataset_path)}' (Baseline) vs. '{os.path.basename(candidate_dataset_path)}' (Candidate)")
            
            # Analyze Candidate
            candidate_results = await self._analyze_single_dataset(
                candidate_dataset_path, runner, judge_runner, embedding_model, opik_client
            )
            
            # Store results
            results[comparison_name] = {
                "baseline": {"path": baseline_dataset_path, "metrics": baseline_results},
                "candidate": {"path": candidate_dataset_path, "metrics": candidate_results}
            }

            # Print comparison report
            print("\n--- COMPARISON REPORT ---")
            self._print_dataset_comparison_report(baseline_results, candidate_results)

        print("\n\n" + "=" * 60)
        print("FULL DATASET ANALYSIS COMPLETE")
        print("=" * 60)
        
        return results

    def _print_dataset_comparison_report(self, baseline: Dict, candidate: Dict):
        """Prints a side-by-side comparison of two dataset analysis results."""
        print(f"{'Metric':<35} | {'Baseline':<15} | {'Candidate':<15}")
        print("-" * 70)
        
        def format_val(val, is_percent=False):
            if isinstance(val, float):
                return f"{val:.2f}%" if is_percent else f"{val:.4f}"
            return str(val)

        metrics_map = {
            "Total Examples": ("total_examples", False),
            "Agent Success Rate": ("agent_performance_success_rate", True),
            "Avg. Complexity (1-5)": ("average_complexity", False),
            "Semantic Diversity Score": ("semantic_diversity_score", False),
            "Redundancy (%)": ("redundancy_percentage", True)
        }

        for name, (key, is_percent) in metrics_map.items():
            b_val = format_val(baseline.get(key, 'N/A'), is_percent)
            c_val = format_val(candidate.get(key, 'N/A'), is_percent)
            print(f"{name:<35} | {b_val:<15} | {c_val:<15}")

    async def compare_agents(self) -> Dict:
        """Compare different agents using the same dataset in a pairwise fashion."""
        print("🚀 AGENT COMPARISON (Pairwise)")
        config = self.config["agent_comparison"]
        
        baseline_agent_config = config["baseline_agent"]
        judge_model_name = config.get("judge_model")

        if not judge_model_name:
            print("ERROR: 'judge_model' must be specified in 'agent_comparison' config.")
            sys.exit(1)

        print(f"Dataset: {config['dataset']}")
        print(f"Baseline Agent: {baseline_agent_config['name']}")
        print(f"Judge Model: {judge_model_name}")

        results = {}

        # Setup services and judge
        session_service = InMemorySessionService()
        judge_model_obj = self._get_model_from_config({"name": judge_model_name})
        judge_agent = Agent(model=judge_model_obj, name="judge_agent", instruction="You are an expert evaluator.")
        judge_runner = Runner(agent=judge_agent, app_name="judge_app", session_service=session_service)

        print("--- Initializing Opik client for tracing ---")
        project_name = os.getenv("OPIK_PROJECT_NAME", "adk-evaluator")
        opik_client = opik.Opik(project_name=project_name)

        # Create baseline agent
        baseline_agent_config = config["baseline_agent"]
        baseline_agent = self._get_agent_from_config(baseline_agent_config)
        setup_opik_tracing(baseline_agent)

        for candidate_agent_config in config.get("candidate_agents", []):
            comparison_name = f"{baseline_agent_config['name']}_vs_{candidate_agent_config['name']}"
            print("-" * 60)
            print(f"Comparing: '{baseline_agent_config['name']}' (Baseline) vs. '{candidate_agent_config['name']}' (Candidate)")
            
            baseline_app_name = f"app_{baseline_agent_config['name']}"
            baseline_runner = Runner(agent=baseline_agent, app_name=baseline_app_name, session_service=session_service)
            
            candidate_agent = self._get_agent_from_config(candidate_agent_config)
            setup_opik_tracing(candidate_agent)
            candidate_app_name = f"app_{candidate_agent_config['name']}"
            candidate_runner = Runner(agent=candidate_agent, app_name=candidate_app_name, session_service=session_service)

            # Load the dataset
            dataset_path = config["dataset"]
            with open(dataset_path, 'r') as f:
                dataset = [json.loads(line) for line in f]

            print(f"Found {len(dataset)} examples in {dataset_path}")
            
            scores = {"wins": 0, "losses": 0, "ties": 0}

            for i, example in enumerate(dataset, 1):
                question = example.get("user_question", "")
                print(f"\n--- Example {i} ---")

                # Setup unique sessions
                baseline_session_id = f"agent_comparison_{comparison_name}_baseline_example_{i}"
                candidate_session_id = f"agent_comparison_{comparison_name}_candidate_example_{i}"
                await self._setup_session(session_service, baseline_runner.app_name, baseline_session_id)
                await self._setup_session(session_service, candidate_runner.app_name, candidate_session_id)
                
                # Get responses
                delay = config.get("delay_seconds", 0.0)
                baseline_response = await self._call_agent(baseline_runner, question, baseline_session_id)
                candidate_response = await self._call_agent(candidate_runner, question, candidate_session_id, delay_seconds=delay)
                
                print(f"  - Baseline response: {baseline_response[:50].strip()}...")
                print(f"  - Candidate response: {candidate_response[:50].strip()}...")

                # Get the verdict
                judge_context = f"agent_comparison_{comparison_name}_judge_example_{i}"
                verdict, reasoning = await self._get_pairwise_judgment(
                    judge_runner, question, baseline_response, candidate_response, context_prefix=judge_context
                )
                
                trace_name = f"agent_comparison:{comparison_name}:example_{i}"
                trace = opik_client.trace(
                    name=trace_name,
                    input={"question": question, "baseline": baseline_response, "candidate": candidate_response},
                    output={"verdict": verdict, "reasoning": reasoning}
                )
                trace.end()

                print(f"  - Verdict: {verdict}")
                print(f"  - Reasoning: {reasoning}")
                
                if verdict == "A":
                    scores["wins"] += 1
                elif verdict == "B":
                    scores["losses"] += 1
                elif verdict == "TIE":
                    scores["ties"] += 1
                
            # Store and print results for this comparison
            print("\n" + "=" * 60)
            print(f"FINAL SCORE for {comparison_name}:")
            print(f"Baseline ({baseline_agent_config['name']}) Wins: {scores['wins']}/{len(dataset)}")
            print(f"Candidate ({candidate_agent_config['name']}) Wins: {scores['losses']}/{len(dataset)}")
            print(f"Ties: {scores['ties']}/{len(dataset)}")
            print("=" * 60)

            results[comparison_name] = {
                "baseline_wins": scores["wins"],
                "candidate_wins": scores['losses'],
                "ties": scores['ties'],
                "total": len(dataset)
            }
        
        return results


# ===========================================================================
# Main
# ===========================================================================

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python src/evaluator.py <mode>")
        print("Modes: model, agent, dataset")
        sys.exit(1)

    mode = sys.argv[1].lower()
    evaluator = AgentEvaluator()

    if mode == "model":
        asyncio.run(evaluator.compare_models())
    elif mode == "agent":
        asyncio.run(evaluator.compare_agents())
    elif mode == "dataset":
        asyncio.run(evaluator.compare_datasets())
    else:
        print(f"Unknown mode: {mode}")
        print("Available modes: model, agent, dataset")
        sys.exit(1)

if __name__ == "__main__":
    main()