"""
Opik Tracing Setup Module

This module provides utilities for setting up Opik tracing on Google ADK agents
using the RecursiveCallbackInjector for automatic recursive injection.
"""

from google.adk.agents import Agent
from opik.integrations.adk.recursive_callback_injector import RecursiveCallbackInjector
from opik.integrations.adk import OpikTracer


def setup_opik_tracing(agent: Agent) -> OpikTracer:
    """Set up Opik tracing on an agent and all its sub-agents/tools recursively."""
    tracer = OpikTracer()
    injector = RecursiveCallbackInjector(tracer=tracer)
    injector.inject(agent)
    return tracer 