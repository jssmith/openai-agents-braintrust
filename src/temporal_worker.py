from __future__ import annotations

import asyncio
import concurrent.futures
from datetime import timedelta

from temporalio import workflow
from temporalio.client import Client
from temporalio.contrib.openai_agents.invoke_model_activity import ModelActivity
from temporalio.contrib.openai_agents.model_parameters import ModelActivityParameters, RetryPolicy
from temporalio.contrib.openai_agents.open_ai_data_converter import (
    open_ai_data_converter,
)
from temporalio.contrib.openai_agents.temporal_openai_agents import (
    set_open_ai_agent_temporal_overrides,
)
from temporalio.worker import Worker

from temporal_workflow import BraintrustDemoAgent

from agents import set_trace_processors, trace
from braintrust import init_logger
from braintrust.wrappers.openai import BraintrustTracingProcessor

async def main():
    with set_open_ai_agent_temporal_overrides(
        ModelActivityParameters(
            start_to_close_timeout=timedelta(seconds=60),
        ),
    ):
        set_trace_processors([BraintrustTracingProcessor(init_logger("openai-agent-with-temporal"))])
        # Create client connected to server at the given address
        client = await Client.connect(
            "localhost:7233",
            data_converter=open_ai_data_converter,
        )
        with trace("haiku agent"):
            model_activity = ModelActivity(model_provider=None)
            worker = Worker(
                client,
                task_queue="openai-agents-task-queue",
                workflows=[
                    BraintrustDemoAgent,
                ],
                activities=[
                    model_activity.invoke_model_activity,
                ],
            )
            await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
