import asyncio
 
from agents import Agent, Runner, set_trace_processors
from braintrust import init_logger
from braintrust.wrappers.openai import BraintrustTracingProcessor
 
 
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
    )
 
    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)
 
 
if __name__ == "__main__":
    set_trace_processors([BraintrustTracingProcessor(init_logger("openai-agent"))])
    asyncio.run(main())