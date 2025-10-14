import asyncio

from agents import ModelSettings, Runner
from openai.types.shared import Reasoning
from tools import code_interpreter, cvm_dfp_composition_query, cvm_dfp_base_query
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
        tools=[
            code_interpreter,
            cvm_dfp_base_query,
            cvm_dfp_composition_query,
        ],
        servers=[],
        model="gpt-5",
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium"), verbosity="medium"
        ),
    )

    inp_data = "Fazer análise fundamentalista da empresa PETR4 (CNPJ 33.000.167/0001-01) em Dezembro de 2024 com cotação a 39 reais. Interpretar resultados e dar recomendações de compra, neutralidade ou venda."
    result = await Runner.run(agent, input=inp_data, max_turns=30)

    for item in result.raw_responses:
        print(item.output)
    # raw_reponses = [f.output for f in result.raw_responses]
    # with open("ELET6.json", "w") as f:
    #     json.dump(raw_reponses, f, indent=4)

    with open("OPCT3.txt", "w") as f:
        f.write(result.final_output)
    await server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
