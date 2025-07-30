"""Concise prompt optimization using EvolutionaryOptimizer."""

import os
import sys
from pathlib import Path

if os.path.exists("src") and "src" not in sys.path:
    sys.path.insert(0, "src")

from opik_evaluation import load_dataset_smartly
from opik_optimizer import EvolutionaryOptimizer, ChatPrompt
from opik.evaluation.metrics import LevenshteinRatio
import opik

def optimize_prompt(agent, current_prompt: str, jsonl_file: str, 
                   optimizer_model: str = "gpt-4o-mini"):
    """Optimize a prompt using EvolutionaryOptimizer with genetic algorithms."""
    
    # Setup
    file_name = Path(jsonl_file).stem
    dataset_name = file_name if file_name.endswith('_dataset') else f"{file_name}_dataset"
    
    # Load data
    client = opik.Opik()
    dataset = load_dataset_smartly(client, dataset_name, jsonl_file)
    
    # Configured optimizer for multi-agent system
    optimizer = EvolutionaryOptimizer(
        model=optimizer_model,
        population_size=30,
        num_generations=15,
        mutation_rate=0.4,
        enable_moo=True,
        enable_llm_crossover=True,
        adaptive_mutation=True,
        output_style_guidance=None,
        infer_output_style=True,
        n_threads=6,
        seed=42,
        temperature=0.3
    )
    
    # Create ChatPrompt object (required by EvolutionaryOptimizer)
    chat_prompt = ChatPrompt(
        name="optimized_prompt",
        system=current_prompt,
        user="{user_question}"
    )
    
    # Evaluation function
    def evaluate_output(dataset_item, llm_output):
        reference = dataset_item.get("expected_output", "")
        if isinstance(reference, dict):
            reference = reference.get("assistant_answer", str(reference))
        return LevenshteinRatio().score(reference=str(reference), output=str(llm_output))
    
    # Run optimization
    result = optimizer.optimize_prompt(
        prompt=chat_prompt,
        dataset=dataset,
        metric=evaluate_output,
        n_samples=25
    )
    
    result.display()
    return result

 