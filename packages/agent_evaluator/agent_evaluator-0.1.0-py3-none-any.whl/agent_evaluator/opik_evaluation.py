import os
import asyncio
import hashlib
import time
from typing import Optional, Dict, Any
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import opik
from opik.evaluation.metrics import Hallucination, AnswerRelevance, ContextRecall, ContextPrecision
from opik.evaluation import evaluate


def load_dataset_smartly(client, dataset_name: str, jsonl_file: str):
    """Load dataset, recreating if content changed. Hashes are now stored inside the
    dedicated 'dataset_hash' directory to avoid cluttering the project root."""
    # Ensure the hash directory exists
    hash_dir = "dataset_hash"
    os.makedirs(hash_dir, exist_ok=True)

    # Location for this dataset's hash file
    hash_file = os.path.join(hash_dir, f"{dataset_name}_hash.txt")
    
    try:
        with open(jsonl_file, 'r') as f:
            current_hash = hashlib.md5(f.read().strip().encode()).hexdigest()
    except FileNotFoundError:
        return client.get_or_create_dataset(name=dataset_name)
    
    # Check if hash matches existing
    try:
        with open(hash_file, 'r') as f:
            if f.read().strip() == current_hash:
                return client.get_dataset(name=dataset_name)
    except FileNotFoundError:
        pass
    
    # Content changed - recreate dataset
    try:
        client.delete_dataset(name=dataset_name)
    except:
        pass
    
    dataset = client.get_or_create_dataset(name=dataset_name)
    dataset.read_jsonl_from_file(jsonl_file)
    
    with open(hash_file, 'w') as f:
        f.write(current_hash)
    
    return dataset


async def call_agent(runner, user_question: str, session_id: str, delay_seconds: float = 0.0):
    """Call agent and return response."""
    if delay_seconds > 0:
        print(f"--- Throttling: Waiting {delay_seconds} seconds before request ---")
        await asyncio.sleep(delay_seconds)
    
    content = types.Content(role='user', parts=[types.Part(text=user_question)])
    
    try:
        async for event in runner.run_async(user_id="eval_user", session_id=session_id, new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts and len(event.content.parts) > 0:
                    return event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    return f"Agent escalated: {event.error_message or 'No message'}"
                break
    except Exception as e:
        return f"Error calling agent: {str(e)}"
    
    return "No response"


def create_task(runner, session_id: str, delay_seconds: float = 0.0):
    """Create evaluation task function."""
    def task(x):
        question = x['user_question']
        expected = x.get('expected_output', {})
        expected_answer = expected.get('assistant_answer', '') if isinstance(expected, dict) else str(expected)
        
        try:
            response = asyncio.run(call_agent(runner, question, session_id, delay_seconds))
        except Exception as e:
            response = f"Error: {str(e)}"
        
        return {
            "input": question,
            "output": response,
            "context": expected_answer,
            "expected_output": expected_answer
        }
    
    return task


async def setup_session(session_service, app_name: str, session_id: str, state: Optional[Dict] = None):
    """Setup evaluation session with cleanup."""
    await session_service.delete_session(app_name=app_name, user_id="eval_user", session_id=session_id)
    await session_service.create_session(app_name=app_name, user_id="eval_user", session_id=session_id, state=state or {})
    print(f"--- Session cleanup: Created fresh session '{session_id}' for evaluation ---")


def run_evaluation(agent, app_name: str, project_name: str, dataset_name: str, jsonl_file: str, 
                  session_state: Optional[Dict] = None, delay_seconds: float = 0.0):
    """Run complete evaluation with optional throttling."""
    if delay_seconds > 0:
        print(f"--- Starting evaluation with {delay_seconds}s delay between requests ---")
    
    # Setup components
    client = opik.Opik()
    session_service = InMemorySessionService()
    runner = Runner(agent=agent, app_name=app_name, session_service=session_service)
    
    # Load dataset and setup session
    dataset = load_dataset_smartly(client, dataset_name, jsonl_file)
    asyncio.run(setup_session(session_service, app_name, "eval_session", session_state))
    
    # Run evaluation
    start_time = time.time()
    result = evaluate(
        dataset=dataset,
        task=create_task(runner, "eval_session", delay_seconds),
        scoring_metrics=[Hallucination(), AnswerRelevance(), ContextRecall(), ContextPrecision()],
        project_name=project_name,
        task_threads=1
    )

    # Attach extracted metrics for downstream use (non-breaking patch)
    try:
        if hasattr(result, 'test_results') and result.test_results:
            # Aggregate metrics across all test_results
            metric_sums = {}
            metric_counts = {}
            n = len(result.test_results)
            for test_result in result.test_results:
                if hasattr(test_result, 'score_results') and test_result.score_results:
                    for score_result in test_result.score_results:
                        if hasattr(score_result, 'name') and hasattr(score_result, 'value'):
                            name = score_result.name
                            value = score_result.value
                            metric_sums[name] = metric_sums.get(name, 0) + value
            # Average each metric over all test_results (use 0 if missing in a test_result)
            avg_metrics = {}
            key_map = {
                'hallucination_metric': 'hallucination',
                'answer_relevance_metric': 'answer_relevance',
                'context_recall_metric': 'context_recall',
                'context_precision_metric': 'context_precision',
            }
            for name in metric_sums:
                avg = metric_sums[name] / n
                norm_name = key_map.get(name, name)
                avg_metrics[norm_name] = avg
            result._extracted_metrics = avg_metrics
    except Exception as e:
        print(f"[WARN] Could not attach extracted metrics: {e}")
    
    if delay_seconds > 0:
        print(f"--- Evaluation completed in {time.time() - start_time:.2f} seconds ---")
    
    return result