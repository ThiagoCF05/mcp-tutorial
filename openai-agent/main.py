import asyncio

from agents import ModelSettings, Runner
from openai.types.shared import Reasoning
from tools import code_interpreter
from servers import get_aws_mcp_server
from financial_agents import get_agent
from financial_agents.financial_analyst import AGENT_INSTRUCTIONS
from dotenv import load_dotenv

load_dotenv()


async def main():
    server = await get_aws_mcp_server()
    await server.connect()
    agent = get_agent(
        name="financial_analyst",
        instructions=AGENT_INSTRUCTIONS,
        tools=[code_interpreter],
        servers=[server],
        model="gpt-5",
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="low"), verbosity="medium"
        ),
    )

    inp_data = "Fazer análise fundamentalista da empresa AURE3 em Dezembro de 2024"
    result = await Runner.run(agent, input=inp_data)
    print(result.final_output)
    await server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
